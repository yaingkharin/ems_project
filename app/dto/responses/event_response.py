from rest_framework import serializers
from app.dto.responses.category_response import CategoryResponse
from app.dto.responses.venue_response import VenueResponse


class EventResponse(serializers.ModelSerializer):
    """
    Serializer for the Event model, including related Category and Venue details.
    """
    category = CategoryResponse(read_only=True)
    venue = VenueResponse(read_only=True)
    image = serializers.SerializerMethodField()
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')
    status = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return f"uploads/{obj.image}"
        return None

    def get_status(self, obj):
        """
        Returns the dynamically computed status:
          - 'cancelled'  → always kept if stored in DB
          - 'upcoming'   → today < event_date, or event hasn't started yet
          - 'ongoing'    → today == event_date and within start/end time
          - 'completed'  → event_date passed or end_time exceeded
        """
        return obj.get_computed_status()

    class Meta:
        from app.models.event import Event
        model = Event
        fields = [
            'id', 'event_name', 'description', 'location', 'event_date',
            'start_time', 'end_time', 'organizer', 'status', 'category', 'venue', 'image',
            'created_at', 'updated_at'
        ]
