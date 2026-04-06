from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse


class EventTicketResponse(serializers.ModelSerializer):
    """
    Serializer for the EventTicket model, including related Booking details.
    """
    booking = BookingResponse(read_only=True)

    class Meta:
        from app.models.event_ticket import EventTicket
        model = EventTicket
        fields = [
            'id', 'booking', 'ticket_code', 'qr_code', 'status', 'created_at', 'updated_at'
        ]
