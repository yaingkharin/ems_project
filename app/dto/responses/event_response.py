from rest_framework import serializers
from app.dto.responses.category_response import CategoryResponse
from app.dto.responses.venue_response import VenueResponse
from app.dto.responses.image_response import ImageResponse


class EventResponse(serializers.ModelSerializer):
    """
    Serializer for the Event model, including related Category and Venue details.
    """
    category = CategoryResponse(read_only=True)
    venue = VenueResponse(read_only=True)
    image = ImageResponse(read_only=True, allow_null=True)

    class Meta:
        from app.models.event import Event
        model = Event
        fields = [
            'id', 'event_name', 'description', 'location', 'event_date',
            'start_time', 'end_time', 'organizer', 'status', 'category', 'venue', 'image',
            'created_at', 'updated_at'
        ]
