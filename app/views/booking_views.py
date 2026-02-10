from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.booking_request import CreateBookingRequest, UpdateBookingRequest
from app.dto.responses.booking_response import BookingResponse
from app.services.booking_service import BookingService
from app.dto.requests.pagination_request import PaginationRequest

from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class BookingListCreateView(APIView):
    """
    Handles listing all bookings and creating a new booking.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_bookings',
        'POST': 'create_bookings',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all bookings.",
        responses={200: BookingResponse(many=True)}
    )
    def get(self, request):
        all_bookings = BookingService.get_all_bookings()
        serializer = BookingResponse(all_bookings, many=True)
        return api_response(data=serializer.data, message="Bookings retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new booking.",
        request_body=CreateBookingRequest,
        responses={
            201: BookingResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateBookingRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            booking = BookingService.create_booking(validated_data)
            response_serializer = BookingResponse(booking)
            return api_response(
                data=response_serializer.data,
                message="Booking created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class BookingRetrieveUpdateDestroyView(APIView):
    """
    Handles retrieving, updating, and deleting a single booking by ID.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_bookings',
        'PUT': 'edit_bookings',
        'DELETE': 'delete_bookings',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single booking by ID.",
        responses={
            200: BookingResponse,
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        booking = BookingService.get_booking_by_id(pk)
        if booking:
            serializer = BookingResponse(booking)
            return api_response(data=serializer.data, message="Booking retrieved successfully.")
        return api_response(message="Booking not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing booking.",
        request_body=UpdateBookingRequest,
        responses={
            200: BookingResponse,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        serializer = UpdateBookingRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        booking = BookingService.update_booking(pk, validated_data)
        if booking:
            response_serializer = BookingResponse(booking)
            return api_response(data=response_serializer.data, message="Booking updated successfully.")
        return api_response(message="Booking not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a booking by ID.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        if BookingService.delete_booking(pk):
            return api_response(message="Booking deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Booking not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedBookingListView(APIView):
    """
    Handles retrieving a paginated list of bookings with optional filtering and searching.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_bookings',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of bookings with optional filtering and searching using a POST request body.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of bookings.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/BookingResponse"
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
            paginated_data = BookingService.get_paginated_bookings(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Bookings retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
