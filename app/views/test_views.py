from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Use the new DTO-named serializers
from app.dto.requests.test_request import CreateTestRequest
from app.dto.responses.test_response import TestResponse

from app.services.test_service import TestService
from app.dto.requests.pagination_request import PaginationRequest

from app.models.test import Test
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class TestListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_tests',
        'POST': 'create_tests',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all tests.",
        responses={200: TestResponse(many=True)}
    )
    def get(self, request):
        tests = TestService.get_all_tests()
        return api_response(data=tests, message="Tests retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new test.",
        request_body=CreateTestRequest,
        responses={
            201: TestResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateTestRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            test_response_dto = TestService.create_test(validated_data)

            return api_response(
                data=test_response_dto,
                message="Test created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class TestRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_tests',
        'PUT': 'edit_tests',
        'DELETE': 'delete_tests',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single test by ID.",
        responses={
            200: TestResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        test = TestService.get_test_by_id(pk)
        if test:
            return api_response(data=test, message="Test retrieved successfully.")
        return api_response(message="Test not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing test.",
        request_body=CreateTestRequest,
        responses={
            200: TestResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = CreateTestRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        test_response_dto = TestService.update_test(pk, validated_data)
        if test_response_dto:
            return api_response(data=test_response_dto, message="Test updated successfully.")
        return api_response(message="Test not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a test by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if TestService.delete_test(pk):
            return api_response(message="Test deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Test not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedTestListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_tests',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of tests with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of tests.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/TestResponse"
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
            paginated_data = TestService.get_paginated_tests(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Tests retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )