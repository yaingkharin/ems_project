from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.role_permission import RolePermission
from app.models.role import Role
from app.models.permission import Permission
 # Added UpdateRolePermissionRequest
from app.dto.requests.pagination_request import PaginationRequest
from app.dto.responses.role_permission_response import RolePermissionResponse

class RolePermissionService:
    @staticmethod
    def create_role_permission(request_data: dict) -> Optional[RolePermissionResponse]:
        try:
            role = Role.objects.get(id=request_data['role_id'])
            permission = Permission.objects.get(id=request_data['permission_id'])
            role_permission = RolePermission.objects.create(role=role, permission=permission)
            return RolePermissionResponse(role_permission).data
        except ObjectDoesNotExist:
            return None # Role or Permission does not exist

    @staticmethod
    def get_role_permission_by_id(rp_id: int) -> Optional[RolePermissionResponse]:
        try:
            role_permission = RolePermission.objects.get(id=rp_id)
            return RolePermissionResponse(role_permission).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_role_permissions() -> List[RolePermissionResponse]:
        role_permissions = RolePermission.objects.all()
        return [RolePermissionResponse(rp).data for rp in role_permissions]

    @staticmethod
    def update_role_permission(rp_id: int, request_data: dict) -> Optional[RolePermissionResponse]:
        try:
            role_permission = RolePermission.objects.get(id=rp_id)
            
            if 'role_id' in request_data:
                role_permission.role = Role.objects.get(id=request_data['role_id'])
            if 'permission_id' in request_data:
                role_permission.permission = Permission.objects.get(id=request_data['permission_id'])

            role_permission.save()
            return RolePermissionResponse(role_permission).data
        except ObjectDoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def delete_role_permission(rp_id: int) -> bool:
        try:
            role_permission = RolePermission.objects.get(id=rp_id)
            role_permission.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_permissions_for_role(role_id: int) -> List[Permission]:
        try:
            role = Role.objects.get(id=role_id)
            return [rp.permission for rp in role.role_permissions.all()]
        except ObjectDoesNotExist:
            return []
        
    @staticmethod
    def get_paginated_role_permissions(validated_data: dict) -> dict:
        page = validated_data.get("page", 1)
        limit = validated_data.get("limit", 100)
        sort_by = validated_data.get("sort_by", "id")
        sort_order = validated_data.get("sort_order", "desc")
        search = validated_data.get("search")
        filters = validated_data.get("filters", {})

        queryset = RolePermission.objects.select_related("role", "permission")

        # Apply filters (allow related lookups with __)
        if filters:
            queryset = queryset.filter(**filters)

        # Apply search
        if search:
            search_query = Q(role__display_name__icontains=search) | Q(permission__display_name__icontains=search)
            queryset = queryset.filter(search_query)

        # Sorting
        sort_field = f"-{sort_by}" if sort_order.lower() == "desc" else sort_by
        queryset = queryset.order_by(sort_field)

        # Pagination
        paginator = Paginator(queryset, limit)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Response
        role_permissions_data = [RolePermissionResponse(rp).data for rp in page_obj.object_list]

        return {
            "data": role_permissions_data,
            "total": paginator.count,
            "page": page_obj.number,
            "limit": limit,
        }

