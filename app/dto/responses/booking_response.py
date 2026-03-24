from rest_framework import serializers
from .common_response import CustomerCustomResponse, EventCustomResponse, TicketCustomResponse


class BookingResponse(serializers.ModelSerializer):
    """
    Custom booking response with only essential data from related models.
    """
    customer = CustomerCustomResponse(read_only=True)
    event = EventCustomResponse(read_only=True)
    ticket = TicketCustomResponse(read_only=True)

    class Meta:
        from app.models.booking import Booking
        model = Booking
        fields = [
            'id', 'customer', 'event', 'ticket', 'quantity', 'total_amount', 
            'status', 'booking_date', 'created_at', 'updated_at'
        ]
