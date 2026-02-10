from rest_framework import serializers


class CreateTicketRequest(serializers.Serializer):
    """
    Serializer for creating a new ticket.
    """
    event_id = serializers.IntegerField()
    ticket_type = serializers.ChoiceField(choices=['VIP', 'Premium', 'Standard'])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    sold = serializers.IntegerField(default=0)


class UpdateTicketRequest(serializers.Serializer):
    """
    Serializer for updating an existing ticket.
    """
    event_id = serializers.IntegerField(required=False)
    ticket_type = serializers.ChoiceField(choices=['VIP', 'Premium', 'Standard'], required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    quantity = serializers.IntegerField(required=False)
    sold = serializers.IntegerField(required=False)