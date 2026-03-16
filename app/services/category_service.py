from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from app.models.category import Category
from app.dto.responses.category_response import CategoryResponse # Fixed import

class CategoryService:
    @staticmethod
    def create_category(request_data: dict) -> Category: # Return type changed to Category model
        category = Category.objects.create(
            category_name=request_data['category_name'],
            description=request_data.get('description', None)
        )
        return category # Return the model instance

    @staticmethod
    def get_category_by_id(id: int) -> Optional[Category]: # Return type changed to Category model
        try:
            return Category.objects.get(id=id, is_deleted=False)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_category() -> List[Category]: # Return type changed to List[Category] model
        return Category.objects.filter(is_deleted=False)

    @staticmethod
    def update_category(id: int, request_data: dict) -> Optional[Category]: # Return type changed to Category model
        try:
            category = Category.objects.get(id=id, is_deleted=False)
            category.category_name = request_data.get('category_name', category.category_name)
            category.description = request_data.get('description', category.description)
            category.save()
            return category
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_category(id: int) -> bool:
        try:
            category = Category.objects.get(id=id)
            category.is_deleted = True
            category.deleted_at = timezone.now()
            category.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_category(id: int) -> bool:
        """
        Permanently delete a category from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            category = Category.objects.get(id=id)
            category.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_categories(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Category.objects.filter(is_deleted=False)

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(category_name__icontains=search) |
                Q(description__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_categories = paginator.page(page)
        except PageNotAnInteger:
            paginated_categories = paginator.page(1)
        except EmptyPage:
            paginated_categories = paginator.page(paginator.num_pages)

        categories_data = CategoryResponse(paginated_categories.object_list, many=True).data # Changed to use CategoryResponse serializer

        return {
            'data': categories_data,
            'total': paginator.count,
            'page': paginated_categories.number,
            'limit': limit,
        }
