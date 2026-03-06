from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.checkin_request import CreateCheckinRequest, UpdateCheckinRequest
from app.dto.responses.checkin_response import CheckinResponse
from app.services.checkin_service import CheckinService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class CheckinListCreateView(APIView):
    """
    Handles listing all check-ins and creating a new check-in.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_checkins',
        'POST': 'create_checkins',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all check-ins.",
        responses={200: CheckinResponse(many=True)}
    )
    def get(self, request):
        all_checkins = CheckinService.get_all_checkins()
        serializer = CheckinResponse(all_checkins, many=True)
        return api_response(data=serializer.data, message="Check-ins retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new check-in.",
        request_body=CreateCheckinRequest,
        responses={
            201: CheckinResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateCheckinRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            checkin = CheckinService.create_checkin(validated_data)
            response_serializer = CheckinResponse(checkin)
            return api_response(
                data=response_serializer.data,
                message="Check-in created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class CheckinRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single check-in by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_checkins',
        'PUT': 'edit_checkins',
        'DELETE': 'delete_checkins',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single check-in by ID.",
        responses={
            200: CheckinResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        checkin = CheckinService.get_checkin_by_id(pk)
        if checkin:
            serializer = CheckinResponse(checkin)
            return api_response(data=serializer.data, message="Check-in retrieved successfully.")
        return api_response(message="Check-in not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing check-in.",
        request_body=UpdateCheckinRequest,
        responses={
            200: CheckinResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateCheckinRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        checkin = CheckinService.update_checkin(pk, validated_data)
        if checkin:
            response_serializer = CheckinResponse(checkin)
            return api_response(data=response_serializer.data, message="Check-in updated successfully.")
        return api_response(message="Check-in not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a check-in by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if CheckinService.delete_checkin(pk):
            return api_response(message="Check-in deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Check-in not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedCheckinListView(APIView):
    """
    Handles retrieving a paginated list of check-ins with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_checkins',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of check-ins with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of check-ins.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/CheckinResponse"
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
            paginated_data = CheckinService.get_paginated_checkins(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Check-ins retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )