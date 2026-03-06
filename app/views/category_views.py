from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Use the new DTO-named serializers
from app.dto.requests.category_request import CreateCategoryRequest, UpdateCategoryRequest # Added UpdateCategoryRequest
from app.dto.responses.category_response import CategoryResponse # Fixed import

from app.services.category_service import CategoryService
from app.dto.requests.pagination_request import PaginationRequest

from app.models.category import Category
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_categories',
        'POST': 'create_categories',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all categories.", # Fixed description
        responses={200: CategoryResponse(many=True)}
    )
    def get(self, request):
        all_categories = CategoryService.get_all_category()
        serializer = CategoryResponse(all_categories, many=True) # Changed to use serializer
        return api_response(data=serializer.data, message="Categories retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new category.", # Fixed description
        request_body=CreateCategoryRequest,
        responses={
            201: CategoryResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateCategoryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            category = CategoryService.create_category(validated_data) # Changed to return model
            response_serializer = CategoryResponse(category) # Serialize model to DTO
            return api_response(
                data=response_serializer.data,
                message="Category created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_categories',
        'PUT': 'edit_categories',
        'DELETE': 'delete_categories',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single category by ID.", # Fixed description
        responses={
            200: CategoryResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        category_by_id = CategoryService.get_category_by_id(pk)
        if category_by_id:
            serializer = CategoryResponse(category_by_id) # Changed to use serializer
            return api_response(data=serializer.data, message="Category retrieved successfully.")
        return api_response(message="Category not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing category.", # Fixed description
        request_body=UpdateCategoryRequest, # Changed to UpdateCategoryRequest
        responses={
            200: CategoryResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateCategoryRequest(data=request.data) # Changed to UpdateCategoryRequest
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        category = CategoryService.update_category(pk, validated_data) # Changed to return model
        if category:
            response_serializer = CategoryResponse(category) # Serialize model to DTO
            return api_response(data=response_serializer.data, message="Category updated successfully.")
        return api_response(message="Category not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a category by ID.", # Fixed description
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if CategoryService.delete_category(pk):
            return api_response(message="Category deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Category not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedCategoryListView(APIView): # Renamed to PaginatedCategoryListView
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_categories',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of categories with optional filtering and searching using a POST request body.", # Fixed description
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of categories.", # Fixed description
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/CategoryResponse"
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
            paginated_data = CategoryService.get_paginated_categories(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Categories retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
