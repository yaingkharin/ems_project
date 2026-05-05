from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from app.models.venue import Venue

from app.dto.responses.venue_response import VenueResponse

class VenueService:
    @staticmethod
    def _resolve_fk(value, model):
        if value is None:
            return None
        if isinstance(value, model):
            return value
        try:
            return model.objects.get(pk=value, is_deleted=False)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_venue(request_data: dict) -> VenueResponse:
        name = request_data['name']
        address = request_data['address']
        contact_info = request_data.get('contact_info')

        # Check for duplicate venue (same name, address, and contact_info)
        duplicate = Venue.objects.filter(
            name__iexact=name,
            address__iexact=address,
            contact_info__iexact=contact_info,
            is_deleted=False
        ).exists()
        if duplicate:
            raise ValueError("Venue with the same Name, Address, and Contact Info already exists.")

        venue = Venue.objects.create(
            name=name,
            address=address,
            contact_info=contact_info
        )
        return VenueResponse(venue).data

    @staticmethod
    def get_venue_by_id(venue_id: int) -> Optional[VenueResponse]:
        try:
            venue = Venue.objects.get(venue_id=venue_id, is_deleted=False)
            return VenueResponse(venue).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_venues() -> List[VenueResponse]:
        venues = Venue.objects.filter(is_deleted=False)
        return [VenueResponse(v).data for v in venues]

    @staticmethod
    def update_venue(venue_id: int, request_data: dict) -> Optional[VenueResponse]:
        try:
            venue = Venue.objects.get(venue_id=venue_id, is_deleted=False)
            new_name = request_data.get('name', venue.name)
            new_address = request_data.get('address', venue.address)
            new_contact_info = request_data.get('contact_info', venue.contact_info)

            # Check for duplicate venue (excluding current venue)
            duplicate = Venue.objects.filter(
                name__iexact=new_name,
                address__iexact=new_address,
                contact_info__iexact=new_contact_info,
                is_deleted=False
            ).exclude(venue_id=venue_id).exists()
            if duplicate:
                raise ValueError("Venue with the same Name, Address, and Contact Info already exists.")

            venue.name = new_name
            venue.address = new_address
            venue.contact_info = new_contact_info
            venue.save()
            return VenueResponse(venue).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_venue(venue_id: int) -> bool:
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            venue.is_deleted = True
            venue.deleted_at = timezone.now()
            venue.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_venue(venue_id: int) -> bool:
        """
        Permanently delete a venue from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            # Use direct Manager to find even soft-deleted items
            venue = Venue.objects.get(venue_id=venue_id)
            venue.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def restore_venue(venue_id: int) -> bool:
        """
        Restore a soft-deleted venue.
        """
        try:
            # Look for soft-deleted item specifically
            venue = Venue.objects.get(venue_id=venue_id, is_deleted=True)
            venue.is_deleted = False
            venue.deleted_at = None
            venue.save()
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

        queryset = Venue.objects.filter(is_deleted=validated_data.get('is_deleted', False))

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