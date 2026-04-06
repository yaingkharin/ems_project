from rest_framework import serializers
from app.models.event_ticket import EventTicket
from app.models.booking import Booking


class CreateEventTicketRequest(serializers.ModelSerializer):
    """
    Serializer used for creating an EventTicket.
    """
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = EventTicket
        fields = [
            'booking', 'ticket_code', 'qr_code', 'status'
        ]


class UpdateEventTicketRequest(serializers.Serializer):
    """
    Serializer used for updating an EventTicket.
    """
    ticket_code = serializers.CharField(required=False, allow_blank=False)
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), required=False)
    qr_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.ChoiceField(choices=EventTicket.STATUS_CHOICES, required=False)

    def validate(self, attrs):
        return attrs
