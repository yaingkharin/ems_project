from rest_framework import serializers
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.event import Event
from app.models.ticket import Ticket


class CreateBookingRequest(serializers.Serializer):
    """Serializer for creating a Booking by customer (self-booking)."""
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=10)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def validate(self, attrs):
        ticket = attrs.get('ticket')
        quantity = attrs.get('quantity')
        if ticket and quantity:
            attrs['total_amount'] = ticket.price * quantity
        return attrs


class AdminCreateBookingRequest(serializers.Serializer):
    """Serializer for admin creating a Booking for any customer."""
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=10)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def validate(self, attrs):
        ticket = attrs.get('ticket')
        quantity = attrs.get('quantity')
        if ticket and quantity:
            attrs['total_amount'] = ticket.price * quantity
        return attrs


class UpdateBookingRequest(serializers.Serializer):
    """Serializer for updating a Booking. All fields optional for partial updates."""
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), required=False)
    quantity = serializers.IntegerField(required=False, min_value=1, max_value=10)
    status = serializers.ChoiceField(choices=['pending', 'confirmed', 'cancelled'], required=False)

    def validate_quantity(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate(self, attrs):
        # add custom validation if needed
        return attrs
