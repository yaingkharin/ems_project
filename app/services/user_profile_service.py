from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.user_profile import UserProfile
from app.models.user import User
from app.dto.responses.user_profile_response import UserProfileResponse


class UserProfileService:
    """
    Service layer for handling user profile related business logic.
    """

    @staticmethod
    def create_user_profile(request_data: dict) -> UserProfile:
        """
        Creates a new user profile.
        """
        user = User.objects.get(id=request_data.pop('user_id'))
        profile = UserProfile.objects.create(
            user=user,
            **request_data
        )
        return profile

    @staticmethod
    def get_user_profile_by_id(profile_id: int) -> Optional[UserProfile]:
        """
        Retrieves a single user profile by its ID.
        """
        try:
            return UserProfile.objects.select_related('user').get(id=profile_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_user_profile_by_user_id(user_id: int) -> Optional[UserProfile]:
        """
        Retrieves a single user profile by user ID.
        """
        try:
            return UserProfile.objects.select_related('user').get(user__id=user_id)
        except ObjectDoesNotExist:
            return None


    @staticmethod
    def get_all_user_profiles() -> List[UserProfile]:
        """
        Retrieves all user profiles.
        """
        return UserProfile.objects.select_related('user').all()

    @staticmethod
    def update_user_profile(profile_id: int, request_data: dict) -> Optional[UserProfile]:
        """
        Updates an existing user profile.
        """
        try:
            profile = UserProfile.objects.get(id=profile_id)

            if 'user_id' in request_data:
                profile.user = User.objects.get(id=request_data.pop('user_id'))

            for key, value in request_data.items():
                setattr(profile, key, value)

            profile.save()
            return profile
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_user_profile(profile_id: int) -> bool:
        """
        Deletes a user profile by its ID.
        """
        try:
            profile = UserProfile.objects.get(id=profile_id)
            profile.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_user_profiles(validated_data: dict) -> dict:
        """
        Retrieves a paginated list of user profiles with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = UserProfile.objects.select_related('user').all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(address__icontains=search) |
                Q(gender__icontains=search) |
                Q(user__email__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_profiles = paginator.page(page)
        except PageNotAnInteger:
            paginated_profiles = paginator.page(1)
        except EmptyPage:
            paginated_profiles = paginator.page(paginator.num_pages)

        profiles_data = UserProfileResponse(paginated_profiles.object_list, many=True).data

        return {
            'data': profiles_data,
            'total': paginator.count,
            'page': paginated_profiles.number,
            'limit': limit,
        }
