from rest_framework import serializers
from app.models.event_registration import EventRegistration
from app.models.user import User
from app.models.event import Event


class CreateEventRegistrationRequest(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = EventRegistration
        fields = ['user', 'event', 'status']


class UpdateEventRegistrationRequest(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    status = serializers.ChoiceField(choices=['pending', 'approved', 'cancelled'], required=False)

    def validate(self, attrs):
        # Custom validations can be added here
        return attrs