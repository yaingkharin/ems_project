from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.payment import Payment
from app.models.booking import Booking
from app.dto.responses.payment_response import PaymentResponse


class PaymentService:
    """
    Service layer for handling payment-related business logic.
    """

    @staticmethod
    def create_payment(request_data: dict) -> Payment:
        """
        Creates a new payment.
        """
        booking = Booking.objects.get(id=request_data.pop('booking_id'))
        payment = Payment.objects.create(
            booking=booking,
            **request_data
        )
        return payment

    @staticmethod
    def get_payment_by_id(payment_id: int) -> Optional[Payment]:
        """
        Retrieves a single payment by its ID.
        """
        try:
            return Payment.objects.select_related('booking').get(id=payment_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_payments() -> List[Payment]:
        """
        Retrieves all payments.
        """
        return Payment.objects.select_related('booking').all()

    @staticmethod
    def update_payment(payment_id: int, request_data: dict) -> Optional[Payment]:
        """
        Updates an existing payment.
        """
        try:
            payment = Payment.objects.get(id=payment_id)

            if 'booking_id' in request_data:
                payment.booking = Booking.objects.get(id=request_data.pop('booking_id'))

            for key, value in request_data.items():
                setattr(payment, key, value)

            payment.save()
            return payment
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_payment(payment_id: int) -> bool:
        """
        Deletes a payment by its ID.
        """
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_payments(validated_data: dict) -> dict:
        """
        Retrieves a paginated list of payments with optional filtering and searching.
        """
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
                Q(method__icontains=search) |
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
