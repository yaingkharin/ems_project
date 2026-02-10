from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.invoice_request import CreateInvoiceRequest, UpdateInvoiceRequest
from app.dto.responses.invoice_response import InvoiceResponse
from app.services.invoice_service import InvoiceService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class InvoiceListCreateView(APIView):
    """
    Handles listing all invoices and creating a new invoice.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_invoices',
        'POST': 'create_invoices',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all invoices.",
        responses={200: InvoiceResponse(many=True)}
    )
    def get(self, request):
        all_invoices = InvoiceService.get_all_invoices()
        serializer = InvoiceResponse(all_invoices, many=True)
        return api_response(data=serializer.data, message="Invoices retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new invoice.",
        request_body=CreateInvoiceRequest,
        responses={
            201: InvoiceResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateInvoiceRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            invoice = InvoiceService.create_invoice(validated_data)
            response_serializer = InvoiceResponse(invoice)
            return api_response(
                data=response_serializer.data,
                message="Invoice created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class InvoiceRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single invoice by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_invoices',
        'PUT': 'edit_invoices',
        'DELETE': 'delete_invoices',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single invoice by ID.",
        responses={
            200: InvoiceResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        invoice = InvoiceService.get_invoice_by_id(pk)
        if invoice:
            serializer = InvoiceResponse(invoice)
            return api_response(data=serializer.data, message="Invoice retrieved successfully.")
        return api_response(message="Invoice not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing invoice.",
        request_body=UpdateInvoiceRequest,
        responses={
            200: InvoiceResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateInvoiceRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        invoice = InvoiceService.update_invoice(pk, validated_data)
        if invoice:
            response_serializer = InvoiceResponse(invoice)
            return api_response(data=response_serializer.data, message="Invoice updated successfully.")
        return api_response(message="Invoice not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an invoice by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if InvoiceService.delete_invoice(pk):
            return api_response(message="Invoice deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Invoice not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedInvoiceListView(APIView):
    """
    Handles retrieving a paginated list of invoices with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_invoices',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of invoices with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of invoices.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/InvoiceResponse"
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
            paginated_data = InvoiceService.get_paginated_invoices(validated_data)

            # Service returns model instances (not serialized). Serialize here in the view
            items = paginated_data.get('items', [])
            serializer = InvoiceResponse(items, many=True)

            response = {
                'data': serializer.data,
                'total': paginated_data.get('total', 0),
                'page': paginated_data.get('page', 1),
                'limit': paginated_data.get('limit', len(serializer.data))
            }

            return api_response(
                data=response,
                message="Paginated Invoices retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )