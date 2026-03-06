from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.dto.requests.image_request import CreateImageRequest
from app.dto.responses.image_response import ImageResponse
from app.services.image_service import ImageService
from app.dto.requests.pagination_request import PaginationRequest
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission


class ImageListCreateView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'all_images',
        'POST': 'create_images',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a list of all images.",
        responses={200: ImageResponse(many=True)}
    )
    def get(self, request):
        images = ImageService.get_all_images()
        return api_response(data=images, message="Images retrieved successfully.")

    @swagger_auto_schema(
        operation_description="Create a new image.",
        request_body=CreateImageRequest,
        responses={201: ImageResponse, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateImageRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            image_response = ImageService.create_image(validated_data)
            return api_response(
                data=image_response,
                message="Image created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_400_BAD_REQUEST)


class ImageRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_images',
        'PUT': 'edit_images',
        'DELETE': 'delete_images',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a single image by ID.",
        responses={200: ImageResponse, 404: "Not Found"}
    )
    def get(self, request, pk):
        image = ImageService.get_image_by_id(pk)
        if image:
            return api_response(data=image, message="Image retrieved successfully.")
        return api_response(message="Image not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing image.",
        request_body=CreateImageRequest,
        responses={200: ImageResponse, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        serializer = CreateImageRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        image_response = ImageService.update_image(pk, validated_data)
        if image_response:
            return api_response(data=image_response, message="Image updated successfully.")
        return api_response(message="Image not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an image by ID.",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        if ImageService.delete_image(pk):
            return api_response(message="Image deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        return api_response(message="Image not found.", success=False, status_code=status.HTTP_404_NOT_FOUND)


class PaginatedImageListView(APIView):
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'all_images',
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of images.",
        request_body=PaginationRequest,
        responses={200: openapi.Response(description="Paginated images")}
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            paginated_data = ImageService.get_paginated_images(validated_data)
            return api_response(
                data=paginated_data,
                message="Paginated Images retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
