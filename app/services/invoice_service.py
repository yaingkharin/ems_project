from typing import Dict, Any
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.models.invoice import Invoice
from app.models.booking import Booking
from app.models.user import User
from django.db.models import Q
import uuid
import datetime


class InvoiceService:
    """
    Service layer for Invoice business logic.

    Notes / design choices:
    - Service methods accept/return Django model instances or simple primitives (not serializers),
      keeping serialization concerns in views/serializers.
    - All DB interactions are performed using Django ORM (no raw SQL).
    - Foreign keys are resolved here if IDs are passed in; but when using the provided serializers
      the booking and user fields will already be model instances.
    """

    @staticmethod
    def _resolve_fk(value, model):
        """Resolve a foreign-key value that may be either an instance or a primary key."""
        if value is None:
            return None
        if isinstance(value, model):
            return value
        return model.objects.get(pk=value)

    @staticmethod
    def get_all_invoices():
        """Return a QuerySet of all invoices."""
        return Invoice.objects.select_related('booking', 'user').all()

    @staticmethod
    def get_invoice_by_id(pk: int):
        """Return an Invoice instance or None if not found."""
        try:
            return Invoice.objects.select_related('booking', 'user').get(pk=pk)
        except Invoice.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_invoice(validated_data: Dict[str, Any]):
        """Create and return an Invoice instance.

        validated_data should be the result of serializer.validated_data.
        booking and user can be either instances or primary keys.
        If invoice_no is missing, generate a unique one.
        """
        # Resolve foreign keys if needed
        booking = InvoiceService._resolve_fk(validated_data.get('booking'), Booking)
        user = InvoiceService._resolve_fk(validated_data.get('user'), User)

        invoice_no = validated_data.get('invoice_no')
        if not invoice_no:
            # Generate a simple unique invoice number if missing
            invoice_no = f"INV-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

        invoice = Invoice.objects.create(
            invoice_no=invoice_no,
            booking=booking,
            user=user,
            total_amount=validated_data.get('total_amount'),
            payment_method=validated_data.get('payment_method'),
            qr_code=validated_data.get('qr_code', None)
        )
        return invoice

    @staticmethod
    @transaction.atomic
    def update_invoice(pk: int, validated_data: Dict[str, Any]):
        """Update the invoice with provided data. Returns the invoice or None if not found."""
        invoice = InvoiceService.get_invoice_by_id(pk)
        if not invoice:
            return None

        # Resolve and set fields if present in validated_data
        if 'booking' in validated_data:
            invoice.booking = InvoiceService._resolve_fk(validated_data.get('booking'), Booking)
        if 'user' in validated_data:
            invoice.user = InvoiceService._resolve_fk(validated_data.get('user'), User)
        if 'invoice_no' in validated_data:
            invoice.invoice_no = validated_data.get('invoice_no')
        if 'total_amount' in validated_data:
            invoice.total_amount = validated_data.get('total_amount')
        if 'payment_method' in validated_data:
            invoice.payment_method = validated_data.get('payment_method')
        if 'qr_code' in validated_data:
            invoice.qr_code = validated_data.get('qr_code')

        invoice.save()
        return invoice

    @staticmethod
    @transaction.atomic
    def delete_invoice(pk: int):
        """Delete the invoice and return True on success, False if not found."""
        invoice = InvoiceService.get_invoice_by_id(pk)
        if not invoice:
            return False
        invoice.delete()
        return True

    @staticmethod
    def get_paginated_invoices(params: Dict[str, Any]):
        """Return a dict with keys: items (list of Invoice instances), total, page, limit.

        params expected keys: page, limit, sort_by, sort_order, search, filters
        filters can include common filter keys like booking_id, user_id, min_total, max_total, date_from, date_to
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = Invoice.objects.select_related('booking', 'user').all()

        # Apply search across invoice_no and payment_method
        if search:
            qs = qs.filter(
                Q(invoice_no__icontains=search) | Q(payment_method__icontains=search)
            )

        # Apply simple filters
        if 'booking_id' in filters:
            qs = qs.filter(booking_id=filters['booking_id'])
        if 'user_id' in filters:
            qs = qs.filter(user_id=filters['user_id'])
        if 'min_total' in filters:
            qs = qs.filter(total_amount__gte=filters['min_total'])
        if 'max_total' in filters:
            qs = qs.filter(total_amount__lte=filters['max_total'])
        if 'date_from' in filters:
            qs = qs.filter(issue_date__gte=filters['date_from'])
        if 'date_to' in filters:
            qs = qs.filter(issue_date__lte=filters['date_to'])

        # Ordering
        order_prefix = '' if sort_order == 'asc' else '-'
        qs = qs.order_by(f"{order_prefix}{sort_by}")

        total = qs.count()
        offset = (page - 1) * limit
        items = list(qs[offset: offset + limit])

        return {
            'items': items,
            'total': total,
            'page': page,
            'limit': limit
        }
