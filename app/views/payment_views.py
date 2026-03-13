from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist

from app.dto.requests.payment_request import CreatePaymentRequest, UpdatePaymentRequest
from app.dto.responses.payment_response import PaymentResponse
from app.services.payment_service import PaymentService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class PaymentListCreateView(APIView):
    """
    Handles listing all payments and creating a new payment.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_payments',
        'POST': 'create_payments',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all payments.",
        responses={200: PaymentResponse(many=True)}
    )
    def get(self, request):
        all_payments = PaymentService.get_all_payments()
        serializer = PaymentResponse(all_payments, many=True)
        return api_response(data=serializer.data, message="Payments retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new payment.",
        request_body=CreatePaymentRequest,
        responses={
            201: PaymentResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreatePaymentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            payment_service = PaymentService()
            result = payment_service.create_payment(validated_data)
            
            response_data = PaymentResponse(result['payment']).data
            message = "Payment created successfully."

            # Append Bakong-specific fields if present
            if result.get('qr_image'):
                response_data = dict(response_data)
                response_data['qr_image'] = result.get('qr_image')
                message = "Payment initiated. Please scan the QR code."

            return api_response(
                data=response_data,
                message=message,
                status_code=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class PaymentRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single payment by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_payments',
        'PUT': 'edit_payments',
        'DELETE': 'delete_payments',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single payment by ID.",
        responses={
            200: PaymentResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        payment = PaymentService.get_payment_by_id(pk)
        if payment:
            serializer = PaymentResponse(payment)
            return api_response(data=serializer.data, message="Payment retrieved successfully.")
        return api_response(message="Payment not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing payment.",
        request_body=UpdatePaymentRequest,
        responses={
            200: PaymentResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdatePaymentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        payment = PaymentService.update_payment(pk, validated_data)
        if payment:
            response_serializer = PaymentResponse(payment)
            return api_response(data=response_serializer.data, message="Payment updated successfully.")
        return api_response(message="Payment not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a payment by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if PaymentService.delete_payment(pk):
            return api_response(message="Payment deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Payment not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedPaymentListView(APIView):
    """
    Handles retrieving a paginated list of payments with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_payments',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of payments with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of payments.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/PaymentResponse"
                            )
                        ),
                        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "limit": openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            paginated_data = PaymentService.get_paginated_payments(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Payments retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )


class GenerateBakongQRView(APIView):
    """
    Handles generating a Bakong KHQR for a payment.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_payments', # Assuming view permission is enough to see QR
    }

    @swagger_auto_schema(
        operation_description="Generate Bakong KHQR for a payment.",
        responses={
            200: openapi.Response(
                description="Bakong QR data.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "qr_data": openapi.Schema(type=openapi.TYPE_STRING),
                        "md5": openapi.Schema(type=openapi.TYPE_STRING),
                        "payment_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        try:
            payment_service = PaymentService() 
            qr_data = payment_service.generate_bakong_qr(pk)
            return api_response(data=qr_data, message="Bakong QR generated successfully.")
        except ObjectDoesNotExist as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class CheckBakongStatusView(APIView):
    """
    Checks Bakong payment status by md5 hash (sent in POST body).
    Mirrors the Express checkPayment endpoint.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'view_payments',
    }

    @swagger_auto_schema(
        operation_description="Check Bakong payment status. Sends the md5 hash to the Bakong API gateway.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['md5'],
            properties={
                'md5': openapi.Schema(type=openapi.TYPE_STRING, description='MD5 hash of the QR payload'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Payment status.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "md5 is required",
            404: "Not Found",
        }
    )
    def post(self, request):
        md5 = request.data.get('md5')
        if not md5:
            return api_response(
                message="md5 is required.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            payment_service = PaymentService()
            result = payment_service.check_bakong_status(md5)

            # Serialize payment if present
            if 'payment' in result:
                result = dict(result)
                result['payment'] = PaymentResponse(result['payment']).data

            is_success = result.get('status') in ('COMPLETED', 'PENDING')
            http_status = status.HTTP_200_OK if is_success else status.HTTP_400_BAD_REQUEST
            
            return api_response(
                data=result,
                message=result.get('message', 'Status checked.'),
                status_code=http_status
            )
        except ObjectDoesNotExist as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestBakongPaymentView(APIView):
    """
    Mock endpoint to test Bakong KHQR generation without database dependencies (no booking/payment models).
    """
    permission_classes = [] # Allow anyone for testing

    @swagger_auto_schema(
        operation_description="Test Bakong KHQR generation without saving to DB.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to pay (e.g. 1.00)'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='USD or KHR'),
            }
        )
    )
    def post(self, request):
        amount = request.data.get('amount', 0.10)
        currency = request.data.get('currency', 'USD')
        
        try:
            from bakong_khqr import KHQR
            from django.conf import settings
            import os
            
            token = getattr(settings, 'BAKONG_ACCESS_TOKEN', os.getenv('BAKONG_ACCESS_TOKEN'))
            account_username = getattr(settings, 'BAKONG_ACCOUNT_USERNAME', os.getenv('BAKONG_ACCOUNT_USERNAME'))
            print('this is bank acc:', account_username)
            
            khqr = KHQR(token)
            
            qr_string = khqr.create_qr(
                bank_account=account_username,
                merchant_name="Test Merchant",
                merchant_city="Phnom Penh",
                amount=float(amount),
                currency=currency,
                store_label="Test Store",
                phone_number="85512345678",
                bill_number="TEST-0001",
                terminal_label="Test Terminal",
            )
            
            md5 = khqr.generate_md5(qr_string)
            qr_image = khqr.qr_image(qr_string, format='base64_uri')
            
            return api_response(
                data={
                    "qr_data": qr_string,
                    "md5": md5,
                    "qr_image": qr_image
                },
                message="Test Bakong QR generated successfully.",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class TestBakongCheckStatusView(APIView):
    """
    Mock endpoint to test checking a Bakong transaction status by MD5 without needing a local database record.
    """
    permission_classes = [] # Allow anyone for testing

    @swagger_auto_schema(
        operation_description="Check Bakong payment status using only the md5 hash. No DB records needed.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['md5'],
            properties={
                'md5': openapi.Schema(type=openapi.TYPE_STRING, description='MD5 hash of the QR payload'),
            }
        )
    )
    def post(self, request):
        md5 = request.data.get('md5')
        if not md5:
            return api_response(
                message="md5 is required.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            from bakong_khqr import KHQR
            from django.conf import settings
            import os
            
            token = getattr(settings, 'BAKONG_ACCESS_TOKEN', os.getenv('BAKONG_ACCESS_TOKEN'))
            khqr = KHQR(token)
            
            # Use the SDK's built-in check payment method
            status_result = khqr.check_payment(md5)
            # This SDK method usually returns "PAID" or "UNPAID" based on API response
            
            # Since check_payment returns a simple string, we can format it nicely
            is_success = status_result == "PAID"
            http_status = status.HTTP_200_OK if is_success else status.HTTP_400_BAD_REQUEST
            message = "Payment confirmed" if is_success else "Payment is pending or failed"

            return api_response(
                data={"status": status_result},
                message=message,
                status_code=http_status
            )
        except Exception as e:
             return api_response(message=str(e), success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
