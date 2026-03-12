import os
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from app.models.event import Event
from app.models.category import Category
from app.models.venue import Venue
from app.dto.responses.event_response import EventResponse

class EventService:

    @staticmethod
    def save_uploaded_file(uploaded_file, subfolder='uploads'):
        upload_dir = os.path.join(settings.MEDIA_ROOT, subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = uploaded_file.name
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{filename.split('.')[0]}_{timezone.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        return f"{settings.MEDIA_URL}{subfolder}/{unique_filename}"

    @staticmethod
    def create_event(request_data: dict) -> Event:
        required_fields = [
            "event_name", "description", "location",
            "event_date", "start_time", "end_time",
            "organizer", "category_id", "venue_id"
        ]

        for field in required_fields:
            if field not in request_data:
                raise ValidationError(f"{field} is required")

        try:
            category = Category.objects.get(id=request_data.pop("category_id"))
        except Category.DoesNotExist:
            raise ValidationError("Invalid category_id")

        try:
            venue = Venue.objects.get(venue_id=request_data.pop("venue_id"))
        except Venue.DoesNotExist:
            raise ValidationError("Invalid venue_id")

        if 'image' in request_data and request_data['image']:
            image_file = request_data.pop('image')
            image_url = EventService.save_uploaded_file(image_file, 'event_images')
            request_data['image'] = image_url

        event = Event.objects.create(
            category=category,
            venue=venue,
            **request_data
        )
        return event

    @staticmethod
    def get_event_by_id(event_id: int) -> Optional[dict]:
        try:
            event = Event.objects.select_related('category', 'venue').get(id=event_id)
            return EventResponse(event).to_dict()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_events() -> List[dict]:
        events = Event.objects.select_related('category', 'venue').all()
        return [EventResponse(e).to_dict() for e in events]

    @staticmethod
    def update_event(event_id: int, request_data: dict) -> Optional[dict]:
        try:
            event = Event.objects.get(id=event_id)

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

            for key, value in request_data.items():
                if key == 'image':
                    if value:
                        event.image = EventService.save_uploaded_file(value, 'event_images')
                    else:
                        event.image = None
                else:
                    setattr(event, key, value)

            event.save()
            return EventResponse(event).to_dict()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_event(event_id: int) -> bool:
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
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_events(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Event.objects.select_related('category', 'venue').all()

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
        except (PageNotAnInteger, EmptyPage):
            paginated_events = paginator.page(1)

        events_data = [EventResponse(e).to_dict() for e in paginated_events.object_list]

        return {
            'data': events_data,
            'total': paginator.count,
            'page': paginated_events.number,
            'limit': limit,
        }