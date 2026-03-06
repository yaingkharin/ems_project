from rest_framework import serializers
from app.models.invoice import Invoice
from app.models.booking import Booking
from app.models.user import User


class CreateInvoiceRequest(serializers.ModelSerializer):
    """
    Serializer used for creating an Invoice.
    - Uses PrimaryKeyRelatedFields for foreign keys so validated_data contains model instances.
    - Keeps validation in the view/serializer layer and leaves business logic to services.
    """
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Invoice
        fields = [
            'invoice_no', 'booking', 'user', 'total_amount', 'payment_method', 'qr_code'
        ]


class UpdateInvoiceRequest(serializers.Serializer):
    """
    Serializer used for updating an Invoice. All fields are optional to support partial updates.
    We don't use ModelSerializer here to allow partial update semantics without requiring an instance.
    """
    invoice_no = serializers.CharField(required=False, allow_blank=False)
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payment_method = serializers.CharField(required=False, allow_blank=False)
    qr_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        # Additional cross-field validation can go here if needed
        return attrs
