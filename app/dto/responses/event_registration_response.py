from rest_framework import serializers
from app.dto.responses.user_response import UserResponse
from app.dto.responses.event_response import EventResponse


class EventRegistrationResponse(serializers.ModelSerializer):
    """
    Serializer for the EventRegistration model, including related User and Event details.
    """
    user = UserResponse(read_only=True)
    event = EventResponse(read_only=True)

    class Meta:
        from app.models.event_registration import EventRegistration
        model = EventRegistration
        fields = [
            'id', 'user', 'event', 'status', 'registered_at',
            'created_at', 'updated_at'
        ]
