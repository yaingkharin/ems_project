from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.customer_request import CreateCustomerRequest
from app.dto.responses.customer_response import CustomerResponse
from app.services.customer_service import CustomerService
from app.dto.requests.pagination_request import PaginationRequest
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class CustomerListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_customers',
        'POST': 'create_customers',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all customers.",
        responses={200: CustomerResponse(many=True)}
    )
    def get(self, request):
        customers = CustomerService.get_all_customers()
        return api_response(data=customers, message="Customers retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new customer.",
        request_body=CreateCustomerRequest,
        responses={201: CustomerResponse, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateCustomerRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            customer_response = CustomerService.create_customer(validated_data)
            return api_response(
                data=customer_response,
                message="Customer created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_customers',
        'PUT': 'edit_customers',
        'DELETE': 'delete_customers',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single customer by ID.",
        responses={200: CustomerResponse, 404: "Not Found"}
    )
    def get(self, request, pk):
        customer = CustomerService.get_customer_by_id(pk)
        if customer:
            return api_response(data=customer, message="Customer retrieved successfully.")
        return api_response(message="Customer not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing customer.",
        request_body=CreateCustomerRequest,
        responses={200: CustomerResponse, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        serializer = CreateCustomerRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        customer_response = CustomerService.update_customer(pk, validated_data)
        if customer_response:
            return api_response(data=customer_response, message="Customer updated successfully.")
        return api_response(message="Customer not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a customer by ID.",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        if CustomerService.delete_customer(pk):
            return api_response(message="Customer deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Customer not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedCustomerListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_customers',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of customers.",
        request_body=PaginationRequest,
        responses={200: openapi.Response(description="Paginated customers")}
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            paginated_data = CustomerService.get_paginated_customers(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Customers retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
