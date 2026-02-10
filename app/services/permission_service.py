from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.permission import Permission

from app.dto.responses.permission_response import PermissionResponse

class PermissionService:
    @staticmethod
    def create_permission(request_data: dict) -> PermissionResponse:
        permission = Permission.objects.create(
            name=request_data['name'],
            display_name=request_data['display_name'],
            group=request_data['group'],
            sort=request_data['sort'],
            status=request_data['status']
        )
        return PermissionResponse(permission).data

    @staticmethod
    def get_permission_by_id(permission_id: int) -> Optional[PermissionResponse]:
        try:
            permission = Permission.objects.get(id=permission_id)
            return PermissionResponse(permission).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_permissions() -> List[PermissionResponse]:
        permissions = Permission.objects.all()
        return [PermissionResponse(permission).data for permission in permissions]

    @staticmethod
    def update_permission(permission_id: int, request_data: dict) -> Optional[PermissionResponse]:
        try:
            permission = Permission.objects.get(id=permission_id)
            permission.name = request_data.get('name', permission.name)
            permission.display_name = request_data.get('display_name', permission.display_name)
            permission.group = request_data.get('group', permission.group)
            permission.sort = request_data.get('sort', permission.sort)
            permission.status = request_data.get('status', permission.status)
            permission.save()
            return PermissionResponse(permission).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_permission(permission_id: int) -> bool:
        try:
            permission = Permission.objects.get(id=permission_id)
            permission.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_permissions(validated_data: dict) -> dict:
        """
        Get paginated permissions with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100) # Consistent default limit
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {}) # Use 'filters' plural

        queryset = Permission.objects.all()

        # Apply filters from the 'filters' dictionary
        if filters:
            queryset = queryset.filter(**filters)

        # Searching
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(group__icontains=search)
            )

        # Sorting
        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_permissions = paginator.page(page)
        except PageNotAnInteger:
            paginated_permissions = paginator.page(1)
        except EmptyPage:
            paginated_permissions = paginator.page(paginator.num_pages)

        permissions_data = [PermissionResponse(p).data for p in paginated_permissions.object_list]

        return {
            'data': permissions_data,
            'total': paginator.count,
            'page': paginated_permissions.number,
            'limit': limit,
        }