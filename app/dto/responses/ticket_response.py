from rest_framework import serializers
from app.dto.responses.event_response import EventResponse


class TicketResponse(serializers.ModelSerializer):
    """
    Serializer for the Ticket model, including related Event details.
    """
    event = EventResponse(read_only=True)

    class Meta:
        from app.models.ticket import Ticket
        model = Ticket
        fields = [
            'id', 'event', 'ticket_type', 'price', 'quantity', 'sold',
            'created_at', 'updated_at'
        ]
