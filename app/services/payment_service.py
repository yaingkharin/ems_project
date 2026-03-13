import os
import logging
import requests
from urllib.parse import quote
from datetime import timedelta
from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone

from bakong_khqr import KHQR

from app.models.payment import Payment
from app.models.booking import Booking
from app.dto.responses.payment_response import PaymentResponse

logger = logging.getLogger(__name__)

BAKONG_EXPIRY_MINUTES = 5


class PaymentService:
    """
    Service layer for handling payment-related business logic, including Bakong integration.
    """

    def __init__(self):
        self.token = os.getenv('BAKONG_ACCESS_TOKEN')
        self.account_username = os.getenv('BAKONG_ACCOUNT_USERNAME')
        self.bakong_api_url = os.getenv(
            'BAKONG_PROD_BASE_API_URL',
            'https://api-bakong.nbc.gov.kh/v1'
        )
        self.khqr_client = KHQR(token=self.token)

    # ------------------------------------------------------------------
    # PAYMENT CRUD
    # ------------------------------------------------------------------

    def create_payment(self, request_data: dict) -> dict:
        """
        Creates a new payment.
        - For 'bakong': generates KHQR with 5-min expiry and returns deep links.
        - For 'cash': immediately marks payment + booking as completed.
        """
        booking_id = request_data.pop('booking_id')
        try:
            booking = Booking.objects.select_related('user', 'event').get(id=booking_id)
        except Booking.DoesNotExist:
            raise ObjectDoesNotExist(f"Booking with id {booking_id} does not exist.")

        payment_method = request_data.get('payment_method', 'cash')
        currency = request_data.get('currency', 'USD')
        amount = booking.total_amount

        if payment_method == 'bakong':
            return self._create_bakong_payment(booking, amount, currency, request_data)
        
        return self._create_cash_payment(booking, amount, request_data)

    def _create_bakong_payment(self, booking: Booking, amount: float, currency: str, request_data: dict) -> dict:
        """Handles the creation of a Bakong payment and generates KHQR payload."""
        expire_at = timezone.now() + timedelta(minutes=BAKONG_EXPIRY_MINUTES)
        
        # Exclude 'amount' from request_data to prevent overriding
        payment_data = {k: v for k, v in request_data.items() if k != 'amount'}
        
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            status='pending',
            description=f"Payment for booking #{booking.id}",
            expire_at=expire_at,
            **payment_data
        )

        try:
            qr_result = self._generate_qr_for_payment(payment, currency)
            payment.refresh_from_db()
            return {
                "payment": payment,
                "qr_image": qr_result.get('qr_image'),
            }
        except Exception as e:
            payment.delete()  # Roll back payment if QR generation fails
            logger.error(f"Failed to generate Bakong QR. Payment rolled back. Error: {str(e)}")
            raise ValueError(f"Failed to generate Bakong payment: {str(e)}")

    def _create_cash_payment(self, booking: Booking, amount: float, request_data: dict) -> dict:
        """Handles the creation of a completed Cash payment."""
        payment_data = {k: v for k, v in request_data.items() if k != 'amount'}

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            status='completed',
            paid=True,
            paid_at=timezone.now(),
            description=f"Payment for booking #{booking.id}",
            **payment_data
        )

        # Mark booking as confirmed immediately since it's a cash payment
        booking.status = 'confirmed'
        booking.save(update_fields=['status', 'updated_at'])

        return {"payment": payment}

    @staticmethod
    def get_payment_by_id(payment_id: int) -> Optional[Payment]:
        """Retrieves a single payment by its ID."""
        try:
            return Payment.objects.select_related('booking').get(id=payment_id)
        except Payment.DoesNotExist:
            return None

    @staticmethod
    def get_all_payments() -> List[Payment]:
        """Retrieves all payments."""
        return Payment.objects.select_related('booking').all()

    @staticmethod
    def update_payment(payment_id: int, request_data: dict) -> Optional[Payment]:
        """Updates an existing payment."""
        try:
            payment = Payment.objects.get(id=payment_id)

            if 'booking_id' in request_data:
                payment.booking = Booking.objects.get(id=request_data.pop('booking_id'))

            for key, value in request_data.items():
                setattr(payment, key, value)

            payment.save()
            return payment
        except Payment.DoesNotExist:
            return None

    @staticmethod
    def delete_payment(payment_id: int) -> bool:
        """Deletes a payment by its ID."""
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.delete()
            return True
        except Payment.DoesNotExist:
            return False

    @staticmethod
    def get_paginated_payments(validated_data: dict) -> dict:
        """Retrieves a paginated list of payments with optional filtering and searching."""
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Payment.objects.select_related('booking').all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(payment_method__icontains=search) |
                Q(status__icontains=search) |
                Q(booking__user__email__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_payments = paginator.page(page)
        except PageNotAnInteger:
            paginated_payments = paginator.page(1)
        except EmptyPage:
            paginated_payments = paginator.page(paginator.num_pages)

        payments_data = PaymentResponse(paginated_payments.object_list, many=True).data

        return {
            'data': payments_data,
            'total': paginator.count,
            'page': paginated_payments.number,
            'limit': limit,
        }

    # ------------------------------------------------------------------
    # BAKONG QR GENERATION
    # ------------------------------------------------------------------

    def generate_bakong_qr(self, payment_id: int) -> dict:
        """Re-generates KHQR for an existing payment (e.g. QR expired)."""
        payment = self.get_payment_by_id(payment_id)
        if not payment:
            raise ObjectDoesNotExist(f"Payment with id {payment_id} does not exist.")
        return self._generate_qr_for_payment(payment, payment.currency or 'USD')

    def _generate_qr_for_payment(self, payment: Payment, currency: str) -> dict:
        """
        Internal helper: generates KHQR payload + MD5 + deep links for a Payment instance.
        Saves qr, md5, deep_link, deep_link_web back to the payment.
        """        
        try:
            amount = float(payment.amount)

            khqr = KHQR(self.token)

            qr_string = khqr.create_qr(
                bank_account=self.account_username,
                merchant_name=payment.merchant_name or "EMS App",
                merchant_city=payment.merchant_city or "Battambang",
                amount=amount,
                currency=currency,
                store_label=payment.store_label or "EMS",
                phone_number=payment.phone_number or "",
                bill_number=payment.bill_number or str(payment.id),
                terminal_label=payment.terminal_label or "EMS Terminal",
            )
            
            md5 = khqr.generate_md5(qr_string)
            qr_image = khqr.qr_image(qr_string, format='base64_uri')

            # Persist back to payment
            payment.qr = qr_string
            payment.md5 = md5
            # We save the generated base64 string directly so it can be retrieved without regenerating
            payment.deep_link = qr_image 
            payment.save(update_fields=['qr', 'md5', 'deep_link'])

            return {
                "qr_data": qr_string,
                "md5": md5,
                "qr_image": qr_image,
                "payment_id": payment.id,
            }
        except Exception as e:
            logger.error(f"Error generating Bakong QR for payment {payment.id}: {str(e)}")
            raise e

    # ------------------------------------------------------------------
    # BAKONG STATUS CHECK  (direct HTTP — matches actual Bakong API)
    # ------------------------------------------------------------------

    def check_bakong_status(self, md5: str) -> dict:
        """
        Checks payment status by calling the Bakong API directly with the md5 hash.
        Mirrors the Express implementation's checkBakongPayment.

        responseCode 0  → COMPLETED
        responseCode 1  → PENDING
        anything else   → FAILED
        """
        # 1. Find payment by md5
        try:
            payment = Payment.objects.select_related('booking').get(md5=md5)
        except Payment.DoesNotExist:
            raise ObjectDoesNotExist("Payment not found for the given md5.")

        # 2. Call Bakong API
        url = f"{self.bakong_api_url}/check_transaction_by_md5"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, json={"md5": md5}, headers=headers, timeout=15)
        except requests.RequestException as e:
            logger.error(f"Bakong HTTP request failed: {str(e)}")
            raise ConnectionError(f"Failed to reach Bakong API: {str(e)}")

        if not response.ok:
            logger.error(f"Bakong HTTP error: {response.status_code} {response.text}")
            raise ConnectionError(f"Bakong service returned error {response.status_code}")

        data = response.json()
        logger.info(f"Bakong response: {data}")

        response_code = data.get('responseCode')

        # 3. Completed
        if response_code == 0:
            if payment.status != 'completed':
                payment.status = 'completed'
                payment.paid = True
                payment.paid_at = timezone.now()
                payment.bakongHash = data.get('data', {}).get('hash')
                payment.fromAccountId = data.get('data', {}).get('fromAccountId')
                payment.toAccountId = data.get('data', {}).get('toAccountId')
                payment.save()

                # Confirm the booking
                booking = payment.booking
                if booking and booking.status != 'confirmed':
                    booking.status = 'confirmed'
                    booking.save(update_fields=['status', 'updated_at'])

            return {
                "status": "COMPLETED",
                "message": "Payment confirmed",
                "payment": payment,
            }

        # 4. Pending
        if response_code == 1:
            return {
                "status": "PENDING",
                "message": data.get('message', 'Payment is pending'),
            }

        # 5. Other errors
        return {
            "status": "FAILED",
            "message": data.get('message', 'Payment failed'),
            "code": response_code,
        }

