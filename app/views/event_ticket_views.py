from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.dto.requests.event_ticket_request import CreateEventTicketRequest, UpdateEventTicketRequest
from app.dto.responses.event_ticket_response import EventTicketResponse
from app.services.event_ticket_service import EventTicketService
from app.dto.requests.pagination_request import PaginationRequest
from app.utils.api_response import api_response


class EventTicketListCreateView(APIView):
    """
    View for listing and creating EventTickets.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all active event tickets.",
        responses={200: EventTicketResponse(many=True)}
    )
    def get(self, request):
        all_event_tickets = EventTicketService.get_all_event_tickets()
        serializer = EventTicketResponse(all_event_tickets, many=True)
        return api_response(data=serializer.data, message="Event tickets retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new event ticket.",
        request_body=CreateEventTicketRequest,
        responses={
            201: EventTicketResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateEventTicketRequest(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            event_ticket = EventTicketService.create_event_ticket(validated_data)
            response_serializer = EventTicketResponse(event_ticket)
            return api_response(
                data=response_serializer.data,
                message="Event ticket created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        return api_response(message=serializer.errors, success=False, status_code=status.HTTP_400_BAD_REQUEST)


class EventTicketRetrieveUpdateDestroyView(APIView):
    """
    View for retrieving, updating, or deleting a specific EventTicket.
    """

    @swagger_auto_schema(
        operation_description="Get a specific event ticket by ID.",
        responses={
            200: EventTicketResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        event_ticket = EventTicketService.get_event_ticket_by_id(pk)
        if event_ticket:
            serializer = EventTicketResponse(event_ticket)
            return api_response(data=serializer.data, message="Event ticket retrieved successfully.")
        return api_response(message="Event ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an event ticket by ID.",
        request_body=UpdateEventTicketRequest,
        responses={
            200: EventTicketResponse,
            404: "Not Found",
            400: "Bad Request"
        }
    )
    def put(self, request, pk):
        serializer = UpdateEventTicketRequest(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            event_ticket = EventTicketService.update_event_ticket(pk, validated_data)
            if event_ticket:
                response_serializer = EventTicketResponse(event_ticket)
                return api_response(data=response_serializer.data, message="Event ticket updated successfully.")
            return api_response(message="Event ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)
        return api_response(message=serializer.errors, success=False, status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete an event ticket by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if EventTicketService.delete_event_ticket(pk):
            return api_response(message="Event ticket deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Event ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedEventTicketListView(APIView):
    """
    View for paginated listing and advanced filtering of EventTickets.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a paginated and filtered list of event tickets using POST with standard pagination format.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, ref="#/definitions/EventTicketResponse")),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
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
            paginated_data = EventTicketService.get_paginated_event_tickets(validated_data)
            items = paginated_data['items']
            response_serializer = EventTicketResponse(items, many=True)

            return api_response(
                data={
                    'data': response_serializer.data,
                    'total': paginated_data['total'],
                    'page': paginated_data['page'],
                    'limit': paginated_data['limit']
                },
                message="Paginated event tickets retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )