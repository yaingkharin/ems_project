from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi # Import openapi for schema definitions

# DTO-named serializers
from app.dto.requests.permission_request import CreatePermissionRequest, UpdatePermissionRequest
from app.dto.responses.permission_response import PermissionResponse

# DTO-named serializers

from app.services.permission_service import PermissionService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission

class PermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_permissions',
        'POST': 'create_permissions',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all permissions.",
        responses={200: PermissionResponse(many=True)}
    )
    def get(self, request):
        permissions = PermissionService.get_all_permissions()
        return api_response(data=permissions, message="Permissions retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new permission.",
        request_body=CreatePermissionRequest,
        responses={
            201: PermissionResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreatePermissionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        permission_response_dto = PermissionService.create_permission(validated_data)

        return api_response(
            data=permission_response_dto,
            message="Permission created successfully.",
            status_code=status.HTTP_201_CREATED
        )


class PermissionRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_permissions',
        'PUT': 'edit_permissions',
        'DELETE': 'delete_permissions',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single permission by ID.",
        responses={
            200: PermissionResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        permission = PermissionService.get_permission_by_id(pk)
        if permission:
            return api_response(data=permission, message="Permission retrieved successfully.")

        return api_response(
            message="Permission not found.",
            success=False,
            status_code=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Update an existing permission.",
        request_body=UpdatePermissionRequest,
        responses={
            200: PermissionResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdatePermissionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data


        permission_response_dto = PermissionService.update_permission(pk, validated_data)

        if permission_response_dto:
            return api_response(
                data=permission_response_dto,
                message="Permission updated successfully."
            )

        return api_response(
            message="Permission not found.",
            success=False,
            status_code=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Delete a permission by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if PermissionService.delete_permission(pk):
            return api_response(
                message="Permission deleted successfully.",
                status_code=status.HTTP_204_NO_CONTENT
            )

        return api_response(
            message="Permission not found.",
            success=False,
            status_code=status.HTTP_404_NOT_FOUND
        )

class PaginatedPermissionListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_permissions',  # Assuming 'all_permissions' is appropriate for paginated listing
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of permissions with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of permissions.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/PermissionResponse"
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
            paginated_data = PermissionService.get_paginated_permissions(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Permissions retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
