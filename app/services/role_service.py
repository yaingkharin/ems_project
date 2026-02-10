from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.role import Role

from app.dto.responses.role_response import RoleResponse

class RoleService:
    @staticmethod
    def create_role(request_data: dict) -> RoleResponse:
        role = Role.objects.create(
            name=request_data['name'],
            display_name=request_data.get('display_name'),
            status=request_data.get('status', True)
        )
        return RoleResponse(role).data

    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[RoleResponse]:
        try:
            role = Role.objects.get(id=role_id)
            return RoleResponse(role).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_roles() -> List[RoleResponse]:
        roles = Role.objects.all()
        return [RoleResponse(role).data for role in roles]

    @staticmethod
    def update_role(role_id: int, request_data: dict) -> Optional[RoleResponse]:
        try:
            role = Role.objects.get(id=role_id)
            role.name = request_data.get('name', role.name)
            role.display_name = request_data.get('display_name', role.display_name)
            role.status = request_data.get('status', role.status)
            role.save()
            return RoleResponse(role).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_role(role_id: int) -> bool:
        try:
            role = Role.objects.get(id=role_id)
            role.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_roles(validated_data: dict) -> dict:
        """
        Get paginated roles with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)  # Consistent default limit
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})  # Use 'filters' plural

        queryset = Role.objects.all()

        # Apply filters from the 'filters' dictionary
        if filters:
            queryset = queryset.filter(**filters)

        # Searching
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(display_name__icontains=search)
            )

        # Sorting
        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_roles = paginator.page(page)
        except PageNotAnInteger:
            paginated_roles = paginator.page(1)
        except EmptyPage:
            paginated_roles = paginator.page(paginator.num_pages)

        roles_data = [RoleResponse(r).data for r in paginated_roles.object_list]

        return {
            'data': roles_data,
            'total': paginator.count,
            'page': paginated_roles.number,
            'limit': limit,
        }