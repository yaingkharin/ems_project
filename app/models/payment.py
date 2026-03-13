from django.db import models
from django.utils import timezone
from app.models.booking import Booking


class Payment(models.Model):
    """
    Represents a payment for a booking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bakong', 'Bakong'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('KHR', 'KHR'),
    ]
    QR_METHOD_CHOICES = [
        ('khqr', 'KHQR'),
        ('usd', 'USD'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES)
    qr_method = models.CharField(max_length=255, null=True, choices=QR_METHOD_CHOICES, default='USD')
    currency = models.CharField(max_length=255, null=True, choices=CURRENCY_CHOICES, default='USD')
    merchant_name = models.CharField(max_length=255, null=True, blank=True, default='EMS App')
    merchant_city = models.CharField(max_length=255, null=True, blank=True, default='Battambang')
    bill_number = models.CharField(max_length=255, null=True, blank=True)
    transaction_ref = models.CharField(max_length=255, null=True, blank=True)
    external_ref = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    store_label = models.CharField(max_length=255, null=True, blank=True)
    terminal_label = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qr = models.CharField(max_length=255, null=True, blank=True)
    md5 = models.CharField(max_length=255, null=True, blank=True)
    bakongHash = models.CharField(max_length=255, null=True, blank=True)
    toAccountId = models.CharField(max_length=255, null=True, blank=True)
    fromAccountId = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)
    deep_link = models.CharField(max_length=500, null=True, blank=True)
    deep_link_web = models.CharField(max_length=500, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"

    class Meta:
        db_table = "payments"
        ordering = ['paid_at']