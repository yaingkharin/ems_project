from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from app.models.image import Image
from app.dto.responses.image_response import ImageResponse


class ImageService:
    @staticmethod
    def create_image(request_data: dict) -> dict:
        image = Image.objects.create(url=request_data['url'])
        return ImageResponse(image).data

    @staticmethod
    def get_image_by_id(image_id: int) -> Optional[dict]:
        try:
            image = Image.objects.get(id=image_id)
            return ImageResponse(image).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_images() -> List[dict]:
        images = Image.objects.all()
        return [ImageResponse(i).data for i in images]

    @staticmethod
    def update_image(image_id: int, request_data: dict) -> Optional[dict]:
        try:
            image = Image.objects.get(id=image_id)
            image.url = request_data.get('url', image.url)
            image.save()
            return ImageResponse(image).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_image(image_id: int) -> bool:
        try:
            image = Image.objects.get(id=image_id)
            image.is_deleted = True
            image.deleted_at = timezone.now()
            image.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_image(image_id: int) -> bool:
        """
        Permanently delete an image from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            image = Image.objects.get(id=image_id)
            image.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_images(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)

        queryset = Image.objects.all()

        if search:
            queryset = queryset.filter(Q(url__icontains=search))

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated = paginator.page(page)
        except PageNotAnInteger:
            paginated = paginator.page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        data = [ImageResponse(i).data for i in paginated.object_list]

        return {
            'data': data,
            'total': paginator.count,
            'page': paginated.number,
            'limit': limit,
        }
