from rest_framework import serializers


class CustomerCustomResponse(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class CategoryCustomResponse(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField()


class VenueCustomResponse(serializers.Serializer):
    venue_id = serializers.IntegerField()
    name = serializers.CharField()


class EventCustomResponse(serializers.Serializer):
    id = serializers.IntegerField()
    event_name = serializers.CharField()
    event_date = serializers.DateField()
    start_time = serializers.TimeField()
    category = CategoryCustomResponse()
    venue = VenueCustomResponse()


class TicketCustomResponse(serializers.Serializer):
    id = serializers.IntegerField()
    ticket_type = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
