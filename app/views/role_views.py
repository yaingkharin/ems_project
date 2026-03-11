from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Use the new DTO-named serializers from api.dto
from app.dto.requests.role_request import CreateRoleRequest, UpdateRoleRequest
from app.dto.responses.role_response import RoleResponse

from app.services.role_service import RoleService
from app.dto.requests.pagination_request import PaginationRequest # Import PaginationRequest

from app.models.role import Role # Import the Role model
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission

class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_roles',
        'POST': 'create_roles',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all roles.",
        responses={200: RoleResponse(many=True)} # Use DTO-named serializer
    )
    def get(self, request):
        roles = RoleService.get_all_roles()
        return api_response(data=roles, message="Roles retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new role.",
        request_body=CreateRoleRequest, # Use DTO-named serializer
        responses={
            201: RoleResponse, # Use DTO-named serializer
            400: "Bad Request"
        }
    )
    def post(self, request):
        # Use the DTO-named serializer for validation
        serializer = CreateRoleRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            role_response_dto = RoleService.create_role(validated_data)
            
            return api_response(data=role_response_dto, message="Role created successfully.", status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)

class RoleRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_roles',
        'PUT': 'edit_roles',
        'DELETE': 'delete_roles',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single role by ID.",
        responses={
            200: RoleResponse, # Use DTO-named serializer
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        role = RoleService.get_role_by_id(pk)
        if role:
            return api_response(data=role, message="Role retrieved successfully.")
        return api_response(message="Role not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing role.",
        request_body=UpdateRoleRequest, # Use DTO-named serializer
        responses={
            200: RoleResponse, # Use DTO-named serializer
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        # Use the DTO-named serializer for validation
        serializer = UpdateRoleRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        role_response_dto = RoleService.update_role(pk, validated_data)
        if role_response_dto:
            return api_response(data=role_response_dto, message="Role updated successfully.")
        return api_response(message="Role not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a role by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if RoleService.delete_role(pk):
            return api_response(message="Role deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Role not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

class PaginatedRoleListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_roles',  # Assuming 'all_roles' is appropriate for paginated listing
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of roles with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of roles.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/RoleResponse"
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
            paginated_data = RoleService.get_paginated_roles(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Roles retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )