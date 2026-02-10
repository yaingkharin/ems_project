from django.db import models
from app.models.booking import Booking
from app.models.user import User


class Invoice(models.Model):
    """
    Represents an invoice for a booking.
    """
    invoice_no = models.CharField(max_length=255, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    issue_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_no} for Booking {self.booking.id}"

    class Meta:
        db_table = "invoices"
        ordering = ['-issue_date']