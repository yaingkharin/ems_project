from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.translation import gettext as _

from app.dto.requests.event_request import CreateEventRequest, UpdateEventRequest
from app.dto.responses.event_response import EventResponse
from app.services.event_service import EventService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class EventListCreateView(APIView):
    """
    Handles listing all events and creating a new event.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_events',
        'POST': 'create_events',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all events.",
        responses={200: EventResponse(many=True)}
    )
    def get(self, request):
        all_events = EventService.get_all_events()
        serializer = EventResponse(all_events, many=True)
        return api_response(data=serializer.data, message=_("Events retrieved successfully."))

    @swagger_auto_schema(
        operation_description="Create a new event.",
        request_body=CreateEventRequest,
        responses={
            201: EventResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateEventRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            event = EventService.create_event(validated_data)
            response_serializer = EventResponse(event)
            return api_response(
                data=response_serializer.data,
                message=_("Event created successfully."),
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single event by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_events',
        'PUT': 'edit_events',
        'DELETE': 'delete_events',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single event by ID.",
        responses={
            200: EventResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        event = EventService.get_event_by_id(pk)
        if event:
            serializer = EventResponse(event)
            return api_response(data=serializer.data, message=_("Event retrieved successfully."))
        return api_response(message=_("Event not found."), success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing event.",
        request_body=UpdateEventRequest,
        responses={
            200: EventResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateEventRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        event = EventService.update_event(pk, validated_data)
        if event:
            response_serializer = EventResponse(event)
            return api_response(data=response_serializer.data, message=_("Event updated successfully."))
        return api_response(message=_("Event not found."), success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a event by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if EventService.delete_event(pk):
            return api_response(message=_("Event deleted successfully."), status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message=_("Event not found."), success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedEventListView(APIView):
    """
    Handles retrieving a paginated list of events with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_events',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of events with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of events.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/EventResponse"
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
            paginated_data = EventService.get_paginated_events(validated_data)
            return api_response(
                data=paginated_data,
                message=_("Paginated Events retrieved successfully.")
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
