from rest_framework import serializers
from app.dto.responses.user_response import UserResponse
from app.dto.responses.event_response import EventResponse
from app.dto.responses.ticket_response import TicketResponse


class BookingResponse(serializers.ModelSerializer):
    """
    Serializer for the Booking model, including related Customer, Event, and Ticket details.
    """
    customer = UserResponse(read_only=True)
    event = EventResponse(read_only=True)
    ticket = TicketResponse(read_only=True)

    class Meta:
        from app.models.booking import Booking
        model = Booking
        fields = [
            'id', 'customer', 'event', 'ticket', 'quantity', 'total_amount', 'status', 'booking_date',
            'created_at', 'updated_at'
        ]
