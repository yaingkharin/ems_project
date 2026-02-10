from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.ticket_request import CreateTicketRequest, UpdateTicketRequest
from app.dto.responses.ticket_response import TicketResponse
from app.services.ticket_service import TicketService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class TicketListCreateView(APIView):
    """
    Handles listing all tickets and creating a new ticket.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_tickets',
        'POST': 'create_tickets',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all tickets.",
        responses={200: TicketResponse(many=True)}
    )
    def get(self, request):
        all_tickets = TicketService.get_all_tickets()
        serializer = TicketResponse(all_tickets, many=True)
        return api_response(data=serializer.data, message="Tickets retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new ticket.",
        request_body=CreateTicketRequest,
        responses={
            201: TicketResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateTicketRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            ticket = TicketService.create_ticket(validated_data)
            response_serializer = TicketResponse(ticket)
            return api_response(
                data=response_serializer.data,
                message="Ticket created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class TicketRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single ticket by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_tickets',
        'PUT': 'edit_tickets',
        'DELETE': 'delete_tickets',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single ticket by ID.",
        responses={
            200: TicketResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        ticket = TicketService.get_ticket_by_id(pk)
        if ticket:
            serializer = TicketResponse(ticket)
            return api_response(data=serializer.data, message="Ticket retrieved successfully.")
        return api_response(message="Ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing ticket.",
        request_body=UpdateTicketRequest,
        responses={
            200: TicketResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateTicketRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        ticket = TicketService.update_ticket(pk, validated_data)
        if ticket:
            response_serializer = TicketResponse(ticket)
            return api_response(data=response_serializer.data, message="Ticket updated successfully.")
        return api_response(message="Ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a ticket by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if TicketService.delete_ticket(pk):
            return api_response(message="Ticket deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Ticket not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedTicketListView(APIView):
    """
    Handles retrieving a paginated list of tickets with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_tickets',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of tickets with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of tickets.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/TicketResponse"
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
            paginated_data = TicketService.get_paginated_tickets(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Tickets retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )