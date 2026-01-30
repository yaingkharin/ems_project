from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Use the new DTO-named serializers from api.dto
from app.dto.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.dto.responses.user_response import UserResponse
from app.services.user_service import UserService
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission
from app.dto.requests.pagination_request import PaginationRequest # Import PaginationRequest

from django.contrib.auth import get_user_model
User = get_user_model() # Get the custom User model

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_users',
        'POST': 'create_users', 
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users.",
        responses={200: UserResponse(many=True)} # Use DTO-named serializer
    )
    def get(self, request):
        users = UserService.get_all_users()
        serializer = UserResponse(users, many=True) # Use DTO-named serializer
        return api_response(data=serializer.data, message="Users retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=CreateUserRequest, # Use DTO-named serializer
        responses={
            201: UserResponse, # Use DTO-named serializer
            400: "Bad Request"
        }
    )
    def post(self, request):
        # Use the DTO-named serializer for validation
        serializer = CreateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            # Create a DTO from validated data for the service layer
            # NOTE: This creates a situation where the "DTO" is actually a DRF Serializer.
            # This is due to the user's specific refactoring request.
            create_user_request_dto = CreateUserRequest(
                email=validated_data['email'],
                password=validated_data['password'],
                username=validated_data['username'],
                role_id=validated_data.get('role_id'),
                status=validated_data.get('status', 'active')
            )
            user_response_dto = UserService.create_user(create_user_request_dto)
            
            # Serialize the DTO response using DRF serializer (now also a DTO-named serializer)
            response_serializer = UserResponse(user_response_dto)
            return api_response(data=response_serializer.data, message="User created successfully.", status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)

class UserRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_users',
        'PUT': 'edit_users',
        'DELETE': 'delete_users',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single user by ID.",
        responses={
            200: UserResponse, # Use DTO-named serializer
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        user = UserService.get_user_by_id(pk)
        if user:
            serializer = UserResponse(user) # Use DTO-named serializer
            return api_response(data=serializer.data, message="User retrieved successfully.")
        return api_response(message="User not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing user.",
        request_body=UpdateUserRequest, # Use DTO-named serializer
        responses={
            200: UserResponse, # Use DTO-named serializer
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        # Use the DTO-named serializer for validation
        serializer = UpdateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Create a DTO from validated data for the service layer
        update_user_request_dto = UpdateUserRequest(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            role_id=validated_data.get('role_id'),
            status=validated_data.get('status')
        )
        user_response_dto = UserService.update_user(pk, update_user_request_dto)
        if user_response_dto:
            response_serializer = UserResponse(user_response_dto) # Use DTO-named serializer
            return api_response(data=response_serializer.data, message="User updated successfully.")
        return api_response(message="User not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a user by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if UserService.delete_user(pk):
            return api_response(message="User deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="User not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedUserListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_users', # Assuming 'all_users' is appropriate for paginated listing
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of users with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of users.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/UserResponse"
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
            paginated_data = UserService.get_paginated_users(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Users retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )