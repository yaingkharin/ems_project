from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.user_profile_request import CreateUserProfileRequest, UpdateUserProfileRequest
from app.dto.responses.user_profile_response import UserProfileResponse
from app.services.user_profile_service import UserProfileService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class UserProfileListCreateView(APIView):
    """
    Handles listing all user profiles and creating a new user profile.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_user_profiles',
        'POST': 'create_user_profiles',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all user profiles.",
        responses={200: UserProfileResponse(many=True)}
    )
    def get(self, request):
        all_profiles = UserProfileService.get_all_user_profiles()
        serializer = UserProfileResponse(all_profiles, many=True)
        return api_response(data=serializer.data, message="User profiles retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new user profile.",
        request_body=CreateUserProfileRequest,
        responses={
            201: UserProfileResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateUserProfileRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            profile = UserProfileService.create_user_profile(validated_data)
            response_serializer = UserProfileResponse(profile)
            return api_response(
                data=response_serializer.data,
                message="User profile created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class UserProfileRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single user profile by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_user_profiles',
        'PUT': 'edit_user_profiles',
        'DELETE': 'delete_user_profiles',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single user profile by ID.",
        responses={
            200: UserProfileResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        profile = UserProfileService.get_user_profile_by_id(pk)
        if profile:
            serializer = UserProfileResponse(profile)
            return api_response(data=serializer.data, message="User profile retrieved successfully.")
        return api_response(message="User profile not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing user profile.",
        request_body=UpdateUserProfileRequest,
        responses={
            200: UserProfileResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateUserProfileRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        profile = UserProfileService.update_user_profile(pk, validated_data)
        if profile:
            response_serializer = UserProfileResponse(profile)
            return api_response(data=response_serializer.data, message="User profile updated successfully.")
        return api_response(message="User profile not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a user profile by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if UserProfileService.delete_user_profile(pk):
            return api_response(message="User profile deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="User profile not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedUserProfileListView(APIView):
    """
    Handles retrieving a paginated list of user profiles with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_user_profiles',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of user profiles with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of user profiles.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/UserProfileResponse"
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
            paginated_data = UserProfileService.get_paginated_user_profiles(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated User Profiles retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
