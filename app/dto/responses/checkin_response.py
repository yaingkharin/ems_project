from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse


class CheckinResponse(serializers.ModelSerializer):
    """
    Serializer for the Checkin model, including related Booking details.
    """
    booking = BookingResponse(read_only=True)

    class Meta:
        from app.models.checkin import Checkin
        model = Checkin
        fields = [
            'id', 'booking', 'ticket_code', 'checkin_time', 'status',
            'created_at', 'updated_at'
        ]