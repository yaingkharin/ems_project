from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse
from app.models.checkin import Checkin


class CheckinResponse(serializers.ModelSerializer):
    """
    Serializer for the Checkin model, including related Booking details.
    """
    booking = BookingResponse(read_only=True, allow_null=True)
    customer_name = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()

    class Meta:
        model = Checkin
        fields = [
            'id', 'booking', 'ticket_code', 'customer_name', 'event_name', 
            'checkin_time', 'status', 'created_at', 'updated_at'
        ]

    def get_customer_name(self, obj):
        if obj.booking and obj.booking.customer:
            first_name = obj.booking.customer.first_name or ""
            last_name = obj.booking.customer.last_name or ""
            name = f"{first_name} {last_name}".strip()
            return name if name else "Unknown"
        return "Unknown"

    def get_event_name(self, obj):
        if obj.booking and obj.booking.event:
            return obj.booking.event.event_name
        return "Unknown"