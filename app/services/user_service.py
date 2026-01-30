from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.role import Role

from app.dto.responses.user_response import UserResponse
from app.utils.bycrypt import hash_password, check_password

User = get_user_model()

class UserService:
    @staticmethod
    def create_user(request_data: dict) -> UserResponse:
        hashed_password = hash_password(request_data['password'])
        role = None
        if request_data.get('role_id'):
            try:
                role = Role.objects.get(id=request_data['role_id'])
            except ObjectDoesNotExist:
                pass 

        user = User.objects.create(
            email=request_data['email'],
            password=hashed_password,
            status=request_data.get('status', 'active'),
            role=role
        )
        return UserResponse(user).data

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserResponse]:
        try:
            user = User.objects.get(id=user_id)
            return UserResponse(user).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_users() -> List[UserResponse]:
        users = User.objects.all()
        return [UserResponse(user).data for user in users]

    @staticmethod
    def update_user(user_id: int, request_data: dict) -> Optional[UserResponse]:
        try:
            user = User.objects.get(id=user_id)
            user.email = request_data.get('email', user.email)
            if 'password' in request_data:
                user.password = hash_password(request_data['password'])
            user.status = request_data.get('status', user.status)
            if 'role_id' in request_data:
                try:
                    role = Role.objects.get(id=request_data['role_id'])
                    user.role = role
                except ObjectDoesNotExist:
                    user.role = None # Set role to None if not found
            user.save()
            return UserResponse(user).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[UserResponse]:
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None # User not found

        if user and check_password(password, user.password):
            return UserResponse(user).data
        return None

    @staticmethod
    def get_paginated_users(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100) # Consistent default limit
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {}) # Use 'filters' plural

        queryset = User.objects.all()

        # Apply filters from the 'filters' dictionary
        if filters:
            queryset = queryset.filter(**filters)

        # Searching
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) | # Assuming first_name is available
                Q(last_name__icontains=search)    # Assuming last_name is available
            )

        # Sorting
        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_users = paginator.page(page)
        except PageNotAnInteger:
            paginated_users = paginator.page(1)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)

        users_data = [UserResponse(u).data for u in paginated_users.object_list]

        return {
            'data': users_data,
            'total': paginator.count,
            'page': paginated_users.number,
            'limit': limit,
        }