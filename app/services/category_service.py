from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Q
from app.models.category import Category

from app.dto.responses.category_ressponse import CategoryResponse

class CategoryService:
    @staticmethod
    def create_category(request_data: dict) -> CategoryResponse:
        category = category.objects.create(
            category_name=request_data['category_name'],
            description=request_data.get('description', None)
            
        )
        return CategoryResponse(category).data

    @staticmethod
    def get_category_by_id(id: int) -> Optional[CategoryResponse]:
        try:
            category_id= Category.objects.get(id=id)
            return CategoryResponse(category_id).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_category() -> List[CategoryResponse]:
        categories = Category.objects.all()
        return [CategoryResponse(v).data for v in categories]

    @staticmethod
    def update_category(id: int, request_data: dict) -> Optional[CategoryResponse]:
        try:
            category = Category.objects.get(id=id)
            category.category_name = request_data.get('category_name', category.category_name)
            category.description = request_data.get('description', category.description)
            category.save()
            return CategoryResponse(category).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_category(id: int) -> bool:
        try:
            category = Category.objects.get(id=id)
            category.delete()
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

        queryset = Category.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(contact_info__icontains=search)
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

        categories_data = [CategoryResponse(v).data for v in paginated_categories.object_list]

        return {
            'data': categories_data,
            'total': paginator.count,
            'page': paginated_categories.number,
            'limit': limit,
        }