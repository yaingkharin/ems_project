from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
            payment = PaymentService.create_payment(validated_data)
            response_serializer = PaymentResponse(payment)
            return api_response(
                data=response_serializer.data,
                message="Payment created successfully.",
                status_code=status.HTTP_201_CREATED
            )
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