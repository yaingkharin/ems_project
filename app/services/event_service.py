from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from app.models.event import Event
from app.models.category import Category
from app.models.venue import Venue
from app.dto.responses.event_response import EventResponse
from app.utils.helper import Helper

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
                raise ValidationError(f"{field} is required")

        # Get Category & Venue safely
        try:
            category = Category.objects.get(id=request_data.pop("category_id"))
        except Category.DoesNotExist:
            raise ValidationError("Invalid category_id")

        try:
            venue = Venue.objects.get(venue_id=request_data.pop("venue_id"))
        except Venue.DoesNotExist:
            raise ValidationError("Invalid venue_id")

        helper = Helper()
        # Handle Image
        image_file = request_data.pop("image", None)
        image_path = None
        if image_file:
            image_path = helper.upload_image(image_file)

        # Handle formatting Dates and Times
        if "event_date" in request_data:
            request_data["event_date"] = helper.format_to_date(request_data["event_date"])
        if "start_time" in request_data:
            request_data["start_time"] = helper.format_to_time(request_data["start_time"])
        if "end_time" in request_data:
            request_data["end_time"] = helper.format_to_time(request_data["end_time"])

        # Create Event
        event = Event.objects.create(
            category=category,
            venue=venue,
            image=image_path,
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
                    raise ValidationError("Invalid category_id")
            if 'venue_id' in request_data:
                try:
                    event.venue = Venue.objects.get(venue_id=request_data.pop('venue_id'))
                except Venue.DoesNotExist:
                    raise ValidationError("Invalid venue_id")

            helper = Helper()
            # Handle Image
            if 'image' in request_data:
                image_file = request_data.pop('image')
                if image_file:
                    new_image_path = helper.update_image(image_file, event.image)
                    if new_image_path:
                        event.image = new_image_path

            # Handle formatting Dates and Times
            if "event_date" in request_data:
                request_data["event_date"] = helper.format_to_date(request_data["event_date"])
            if "start_time" in request_data:
                request_data["start_time"] = helper.format_to_time(request_data["start_time"])
            if "end_time" in request_data:
                request_data["end_time"] = helper.format_to_time(request_data["end_time"])

            # Update other fields
            for key, value in request_data.items():
                setattr(event, key, value)

            event.save()
            return event
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def soft_delete_event(event_id: int) -> bool:
        """
        Soft deletes an event by its ID.
        """
        try:
            event = Event.objects.get(id=event_id)
            event.is_deleted = True
            event.deleted_at = timezone.now()
            event.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_event(event_id: int) -> bool:
        """
        Permanently delete an event from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            event = Event.objects.get(id=event_id)
            event.delete()  # Hard delete
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
