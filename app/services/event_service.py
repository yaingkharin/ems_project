from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.translation import gettext as _
from app.models.event import Event
from app.models.category import Category
from app.models.venue import Venue
from app.dto.responses.event_response import EventResponse

class EventService:
    """
    Service layer for handling event-related business logic.
    """

    @staticmethod
    def create_event(request_data: dict) -> Event:
        """
        Creates a new event with validation.
        """
        required_fields = [
            "event_name", "description", "location",
            "event_date", "start_time", "end_time",
            "organizer", "category_id", "venue_id"
        ]

        # Validate required fields
        for field in required_fields:
            if field not in request_data:
                raise ValidationError(_("%(field)s is required") % {"field": field})

        # Get Category & Venue safely
        try:
            category = Category.objects.get(id=request_data.pop("category_id"))
        except Category.DoesNotExist:
            raise ValidationError(_("Invalid category_id"))

        try:
            venue = Venue.objects.get(venue_id=request_data.pop("venue_id"))
        except Venue.DoesNotExist:
            raise ValidationError(_("Invalid venue_id"))

        # Create Event
        event = Event.objects.create(
            category=category,
            venue=venue,
            **request_data
        )
        return event

    @staticmethod
    def get_event_by_id(event_id: int) -> Optional[Event]:
        """
        Retrieves a single event by its ID.
        """
        try:
            return Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_events() -> List[Event]:
        """
        Retrieves all events.
        """
        return Event.objects.all()

    @staticmethod
    def update_event(event_id: int, request_data: dict) -> Optional[Event]:
        """
        Updates an existing event safely.
        """
        try:
            event = Event.objects.get(id=event_id)

            # Update Category / Venue if provided
            if 'category_id' in request_data:
                try:
                    event.category = Category.objects.get(id=request_data.pop('category_id'))
                except Category.DoesNotExist:
                    raise ValidationError(_("Invalid category_id"))
            if 'venue_id' in request_data:
                try:
                    event.venue = Venue.objects.get(venue_id=request_data.pop('venue_id'))
                except Venue.DoesNotExist:
                    raise ValidationError(_("Invalid venue_id"))

            # Update other fields
            for key, value in request_data.items():
                setattr(event, key, value)

            event.save()
            return event
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_event(event_id: int) -> bool:
        """
        Deletes an event by its ID.
        """
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_events(validated_data: dict) -> dict:
        """
        Retrieves a paginated list of events with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Event.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(event_name__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search) |
                Q(organizer__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_events = paginator.page(page)
        except PageNotAnInteger:
            paginated_events = paginator.page(1)
        except EmptyPage:
            paginated_events = paginator.page(paginator.num_pages)

        events_data = EventResponse(paginated_events.object_list, many=True).data

        return {
            'data': events_data,
            'total': paginator.count,
            'page': paginated_events.number,
            'limit': limit,
        }
