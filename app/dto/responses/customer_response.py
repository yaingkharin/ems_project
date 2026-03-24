from rest_framework import serializers
from app.models.customer import Customer

class CustomerResponse(serializers.ModelSerializer):
    # role = RoleResponse(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'picture', 'email_verified', 'status', 'created_at', 'updated_at']
