from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.event_registration_request import CreateEventRegistrationRequest, UpdateEventRegistrationRequest
from app.dto.responses.event_registration_response import EventRegistrationResponse
from app.services.event_registration_service import EventRegistrationService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class EventRegistrationListCreateView(APIView):
    """
    Handles listing all event registrations and creating a new event registration.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_event_registrations',
        'POST': 'create_event_registrations',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all event registrations.",
        responses={200: EventRegistrationResponse(many=True)}
    )
    def get(self, request):
        all_registrations = EventRegistrationService.get_all_event_registrations()
        serializer = EventRegistrationResponse(all_registrations, many=True)
        return api_response(data=serializer.data, message="Event registrations retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new event registration.",
        request_body=CreateEventRegistrationRequest,
        responses={
            201: EventRegistrationResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateEventRegistrationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            registration = EventRegistrationService.create_event_registration(validated_data)
            response_serializer = EventRegistrationResponse(registration)
            return api_response(
                data=response_serializer.data,
                message="Event registration created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class EventRegistrationRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single event registration by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_event_registrations',
        'PUT': 'edit_event_registrations',
        'DELETE': 'delete_event_registrations',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single event registration by ID.",
        responses={
            200: EventRegistrationResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        registration = EventRegistrationService.get_event_registration_by_id(pk)
        if registration:
            serializer = EventRegistrationResponse(registration)
            return api_response(data=serializer.data, message="Event registration retrieved successfully.")
        return api_response(message="Event registration not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing event registration.",
        request_body=UpdateEventRegistrationRequest,
        responses={
            200: EventRegistrationResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateEventRegistrationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        registration = EventRegistrationService.update_event_registration(pk, validated_data)
        if registration:
            response_serializer = EventRegistrationResponse(registration)
            return api_response(data=response_serializer.data, message="Event registration updated successfully.")
        return api_response(message="Event registration not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an event registration by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if EventRegistrationService.delete_event_registration(pk):
            return api_response(message="Event registration deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Event registration not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedEventRegistrationListView(APIView):
    """
    Handles retrieving a paginated list of event registrations with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_event_registrations',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of event registrations with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of event registrations.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/EventRegistrationResponse"
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
            paginated_data = EventRegistrationService.get_paginated_event_registrations(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Event Registrations retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )