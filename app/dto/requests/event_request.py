from rest_framework import serializers

class CreateEventRequest(serializers.Serializer):
    """
    Serializer for creating a new event.
    """
    event_name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    location = serializers.CharField(max_length=255)
    event_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    organizer = serializers.CharField(max_length=255)
    category_id = serializers.IntegerField()
    venue_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['planned', 'ongoing', 'completed'], default='planned')

class UpdateEventRequest(serializers.Serializer):
    """
    Serializer for updating an existing event.
    """
    event_name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(max_length=255, required=False)
    event_date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    organizer = serializers.CharField(max_length=255, required=False)
    category_id = serializers.IntegerField(required=False)
    venue_id = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=['planned', 'ongoing', 'completed'], required=False)