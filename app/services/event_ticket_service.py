from typing import Dict, Any
from django.db import transaction
from django.utils import timezone
from app.models.event_ticket import EventTicket
from app.models.booking import Booking
from django.db.models import Q
import uuid
import datetime
import qrcode
import io
import base64


class EventTicketService:
    """
    Service layer for EventTicket business logic.
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
    def get_all_event_tickets():
        """Return a QuerySet of all event tickets."""
        return EventTicket.objects.select_related('booking').filter(is_deleted=False)

    @staticmethod
    def get_event_ticket_by_id(pk: int):
        """Return an EventTicket instance or None if not found."""
        try:
            return EventTicket.objects.select_related('booking').get(pk=pk, is_deleted=False)
        except EventTicket.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_event_ticket(validated_data: Dict[str, Any]):
        """Create and return an EventTicket instance.
        """
        # Resolve foreign keys if needed
        booking = EventTicketService._resolve_fk(validated_data.get('booking'), Booking)

        ticket_code = validated_data.get('ticket_code')
        if not ticket_code:
            # Generate a unique ticket code if missing
            ticket_code = f"TKT-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

        qr_code = validated_data.get('qr_code', None)
        if not qr_code:
            # Generate QR code for the ticket_code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(ticket_code)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode()
            qr_code = f"data:image/png;base64,{qr_base64}"

        event_ticket = EventTicket.objects.create(
            ticket_code=ticket_code,
            booking=booking,
            qr_code=qr_code,
            status=validated_data.get('status', 'UNUSED')
        )
        return event_ticket

    @staticmethod
    @transaction.atomic
    def update_event_ticket(pk: int, validated_data: Dict[str, Any]):
        """Update the event ticket with provided data. Returns the event ticket or None if not found."""
        event_ticket = EventTicketService.get_event_ticket_by_id(pk)
        if not event_ticket:
            return None

        # Resolve and set fields if present in validated_data
        if 'booking' in validated_data:
            event_ticket.booking = EventTicketService._resolve_fk(validated_data.get('booking'), Booking)
        if 'ticket_code' in validated_data:
            event_ticket.ticket_code = validated_data.get('ticket_code')
        if 'qr_code' in validated_data:
            event_ticket.qr_code = validated_data.get('qr_code')
        if 'status' in validated_data:
            event_ticket.status = validated_data.get('status')

        event_ticket.save()
        return event_ticket

    @staticmethod
    @transaction.atomic
    def delete_event_ticket(pk: int):
        """Soft delete the event ticket and return True on success, False if not found."""
        event_ticket = EventTicketService.get_event_ticket_by_id(pk)
        if not event_ticket:
            return False
        event_ticket.is_deleted = True
        event_ticket.deleted_at = timezone.now()
        event_ticket.save()
        return True

    @staticmethod
    @transaction.atomic
    def force_delete_event_ticket(pk: int):
        """
        Permanently delete an event ticket from the database.
        """
        event_ticket = EventTicketService.get_event_ticket_by_id(pk)
        if not event_ticket:
            return False
        event_ticket.delete()  # Hard delete
        return True

    @staticmethod
    def get_paginated_event_tickets(params: Dict[str, Any]):
        """Return a dict with keys: items (list of EventTicket instances), total, page, limit.
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = EventTicket.objects.select_related('booking').filter(is_deleted=False)

        # Apply search across ticket_code
        if search:
            qs = qs.filter(
                Q(ticket_code__icontains=search)
            )

        # Apply simple filters
        if 'booking_id' in filters:
            qs = qs.filter(booking_id=filters['booking_id'])
        if 'booking.id' in filters:
            qs = qs.filter(booking_id=filters['booking.id'])
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])

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
