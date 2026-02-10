from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.venue_request import CreateVenueRequest

from app.dto.responses.venue_response import VenueResponse
from app.services.venue_service import VenueService
from app.dto.requests.pagination_request import PaginationRequest
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class VenueListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_venues',
        'POST': 'create_venues',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all venues.",
        responses={200: VenueResponse(many=True)}
    )
    def get(self, request):
        venues = VenueService.get_all_venues()
        return api_response(data=venues, message="Venues retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new venue.",
        request_body=CreateVenueRequest,
        responses={201: VenueResponse, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateVenueRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            venue_response_dto = VenueService.create_venue(validated_data)
            return api_response(
                data=venue_response_dto,
                message="Venue created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class VenueRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_venues',
        'PUT': 'edit_venues',
        'DELETE': 'delete_venues',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single venue by ID.",
        responses={200: VenueResponse, 404: "Not Found"}
    )
    def get(self, request, pk):
        venue = VenueService.get_venue_by_id(pk)
        if venue:
            return api_response(data=venue, message="Venue retrieved successfully.")
        return api_response(message="Venue not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing venue.",
        request_body=CreateVenueRequest,
        responses={200: VenueResponse, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        serializer = CreateVenueRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        venue_response_dto = VenueService.update_venue(pk, validated_data)
        if venue_response_dto:
            return api_response(data=venue_response_dto, message="Venue updated successfully.")
        return api_response(message="Venue not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a venue by ID.",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        if VenueService.delete_venue(pk):
            return api_response(message="Venue deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Venue not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedVenueListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_venues',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of venues with optional filtering and searching.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="Paginated list of venues.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                ref="#/definitions/VenueResponse"
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
            paginated_data = VenueService.get_paginated_venues(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Venues retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )