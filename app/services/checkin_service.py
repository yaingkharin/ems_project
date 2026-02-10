from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.checkin import Checkin
from app.models.booking import Booking
from app.dto.responses.checkin_response import CheckinResponse


class CheckinService:
    """
    Service layer for handling check-in related business logic.
    """

    @staticmethod
    def create_checkin(request_data: dict) -> Checkin:
        """
        Creates a new check-in.
        """
        booking = Booking.objects.get(id=request_data.pop('booking_id'))
        checkin = Checkin.objects.create(
            booking=booking,
            **request_data
        )
        return checkin

    @staticmethod
    def get_checkin_by_id(checkin_id: int) -> Optional[Checkin]:
        """
        Retrieves a single check-in by its ID.
        """
        try:
            return Checkin.objects.select_related('booking').get(id=checkin_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_checkins() -> List[Checkin]:
        """
        Retrieves all check-ins.
        """
        return Checkin.objects.select_related('booking').all()

    @staticmethod
    def update_checkin(checkin_id: int, request_data: dict) -> Optional[Checkin]:
        """
        Updates an existing check-in.
        """
        try:
            checkin = Checkin.objects.get(id=checkin_id)

            if 'booking_id' in request_data:
                checkin.booking = Booking.objects.get(id=request_data.pop('booking_id'))

            for key, value in request_data.items():
                setattr(checkin, key, value)

            checkin.save()
            return checkin
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_checkin(checkin_id: int) -> bool:
        """
        Deletes a check-in by its ID.
        """
        try:
            checkin = Checkin.objects.get(id=checkin_id)
            checkin.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_checkins(validated_data: dict) -> dict:
        """
        Retrieves a paginated list of check-ins with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Checkin.objects.select_related('booking').all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(ticket_code__icontains=search) |
                Q(status__icontains=search) |
                Q(booking__id__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_checkins = paginator.page(page)
        except PageNotAnInteger:
            paginated_checkins = paginator.page(1)
        except EmptyPage:
            paginated_checkins = paginator.page(paginator.num_pages)

        checkins_data = CheckinResponse(paginated_checkins.object_list, many=True).data

        return {
            'data': checkins_data,
            'total': paginator.count,
            'page': paginated_checkins.number,
            'limit': limit,
        }
