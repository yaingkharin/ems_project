from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Q
from app.models.venue import Venue

from app.dto.responses.venue_response import VenueResponse

class VenueService:
    @staticmethod
    def create_venue(request_data: dict) -> VenueResponse:
        venue = Venue.objects.create(
            name=request_data['name'],
            address=request_data['address'],
            capacity=request_data['capacity'],
            contact_info=request_data.get('contact_info')
        )
        return VenueResponse(venue).data

    @staticmethod
    def get_venue_by_id(venue_id: int) -> Optional[VenueResponse]:
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            return VenueResponse(venue).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_venues() -> List[VenueResponse]:
        venues = Venue.objects.all()
        return [VenueResponse(v).data for v in venues]

    @staticmethod
    def update_venue(venue_id: int, request_data: dict) -> Optional[VenueResponse]:
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            venue.name = request_data.get('name', venue.name)
            venue.address = request_data.get('address', venue.address)
            venue.capacity = request_data.get('capacity', venue.capacity)
            venue.contact_info = request_data.get('contact_info', venue.contact_info)
            venue.save()
            return VenueResponse(venue).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_venue(venue_id: int) -> bool:
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            venue.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_venues(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'venue_id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Venue.objects.all()

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
            paginated_venues = paginator.page(page)
        except PageNotAnInteger:
            paginated_venues = paginator.page(1)
        except EmptyPage:
            paginated_venues = paginator.page(paginator.num_pages)

        venues_data = [VenueResponse(v).data for v in paginated_venues.object_list]

        return {
            'data': venues_data,
            'total': paginator.count,
            'page': paginated_venues.number,
            'limit': limit,
        }