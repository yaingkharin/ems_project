from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Use the new DTO-named serializers from api.dto
from app.dto.requests.role_permission_request import CreateRolePermissionRequest, UpdateRolePermissionRequest
from app.dto.responses.role_permission_response import RolePermissionResponse
from app.dto.responses.permission_response import PermissionResponse
from app.dto.requests.pagination_request import PaginationRequest

from app.services.role_permission_service import RolePermissionService
from app.models.role import Role

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class RolePermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_role_permissions',
        'POST': 'create_role_permissions',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all role permissions.",
        responses={200: RolePermissionResponse(many=True)}
    )
    def get(self, request):
        role_permissions = RolePermissionService.get_all_role_permissions()
        return api_response(data=role_permissions, message="Role Permissions retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new role-permission assignment.",
        request_body=CreateRolePermissionRequest,
        responses={
            201: RolePermissionResponse,
            400: "Bad Request",
            404: "Role or Permission not found"
        }
    )
    def post(self, request):
        serializer = CreateRolePermissionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            role_permission_response_dto = RolePermissionService.create_role_permission(validated_data)

            if role_permission_response_dto:
                return api_response(
                    data=role_permission_response_dto,
                    message="Role Permission created successfully.",
                    status_code=status.HTTP_201_CREATED
                )

            return api_response(
                message="Role or Permission not found.",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )


class RolePermissionRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_role_permissions',
        'PUT': 'edit_role_permissions',
        'DELETE': 'delete_role_permissions',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single role-permission assignment by ID.",
        responses={
            200: RolePermissionResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        role_permission = RolePermissionService.get_role_permission_by_id(pk)

        if role_permission:
            return api_response(
                data=role_permission,
                message="Role Permission retrieved successfully."
            )

        return api_response(
            message="Role Permission not found.",
            success=False,
            status_code=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Update an existing role-permission assignment.",
        request_body=UpdateRolePermissionRequest,
        responses={
            200: RolePermissionResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateRolePermissionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not validated_data:
            return api_response(
                message="No data provided for update.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            updated_role_permission_response_dto = RolePermissionService.update_role_permission(
                pk,
                validated_data
            )

            if updated_role_permission_response_dto:
                return api_response(
                    data=updated_role_permission_response_dto,
                    message="Role Permission updated successfully."
                )

            return api_response(
                message="Role or Permission not found.",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Delete a role-permission assignment by ID.",
        responses={
            200: openapi.Response(description="Role Permission deleted successfully."),
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        try:
            deleted = RolePermissionService.delete_role_permission(pk)
            if deleted:
                return api_response(
                    message="Role Permission deleted successfully."
                )

            return api_response(
                message="Role Permission not found.",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

class RolePermissionsListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_role_permissions',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all permissions associated with a specific role ID.",
        responses={
            200: PermissionResponse(many=True),
            404: "Role not found"
        }
    )
    def get(self, request, role_id):
        try:
            # Check if the role exists
            role_exists = Role.objects.filter(id=role_id).exists()
            if not role_exists:
                return api_response(
                    message=f"Role with ID {role_id} not found.",
                    success=False,
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            permissions = RolePermissionService.get_permissions_for_role(role_id)
            serializer = PermissionResponse(permissions, many=True)
            return api_response(
                data=serializer.data,
                message=f"Permissions for Role ID {role_id} retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

class PaginatedRolePermissionListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_role_permissions', # Changed from GET
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of role permissions with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,  # Changed from query_serializer
        responses={
            200: openapi.Response(
                description="Paginated list of role permissions.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/RolePermissionResponse"
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
            paginated_data = RolePermissionService.get_paginated_role_permissions(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Role Permissions retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
