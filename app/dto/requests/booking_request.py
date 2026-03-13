from rest_framework import serializers
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event


class CreateBookingRequest(serializers.ModelSerializer):
    """Serializer for creating a Booking. Uses PrimaryKeyRelatedFields for FKs."""
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Booking
        fields = [
            'customer', 'event', 'quantity', 'total_amount', 'status'
        ]


class UpdateBookingRequest(serializers.Serializer):
    """Serializer for updating a Booking. All fields optional for partial updates."""
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    quantity = serializers.IntegerField(required=False)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    status = serializers.ChoiceField(choices=['pending', 'confirmed', 'cancelled'], required=False)

    def validate(self, attrs):
        # add custom validation if needed
        return attrs
