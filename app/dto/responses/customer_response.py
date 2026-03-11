from rest_framework import serializers
from app.models.customer import Customer


class CustomerResponse(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """

    class Meta:
        model = Customer
        fields = ['id', 'username', 'gmail']
