from typing import Dict, Any
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.event import Event
from app.models.ticket import Ticket


class BookingService:
    @staticmethod
    def _resolve_fk(value, model):
        if value is None:
            return None
        if isinstance(value, model):
            return value
        try:
            # Only resolve objects that are NOT soft-deleted
            return model.objects.get(pk=value, is_deleted=False)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_bookings():
        return Booking.objects.select_related('customer', 'event', 'ticket').filter(is_deleted=False)

    @staticmethod
    def get_booking_by_id(pk: int):
        try:
            return Booking.objects.select_related('customer', 'event', 'ticket').get(pk=pk, is_deleted=False)
        except Booking.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_booking(validated_data: Dict[str, Any]):
        customer = BookingService._resolve_fk(validated_data.get('customer'), Customer)
        if not customer:
            raise ValueError('Customer is required')
        
        event = BookingService._resolve_fk(validated_data.get('event'), Event)
        ticket = BookingService._resolve_fk(validated_data.get('ticket'), Ticket)

        quantity = validated_data.get('quantity')
        total_amount = validated_data.get('total_amount')

        # Basic ticket availability check
        if ticket and quantity and ticket.quantity - ticket.sold < quantity:
            raise ValueError('Not enough tickets available')

        status_val = validated_data.get('status', 'pending')
        booking = Booking.objects.create(
            customer=customer,
            event=event,
            ticket=ticket,
            quantity=quantity,
            total_amount=total_amount,
            status=status_val
        )

        # Update ticket sold count ONLY if confirmed
        if status_val == 'confirmed' and ticket and quantity:
            ticket.sold += quantity
            ticket.save()

        return booking

    @staticmethod
    @transaction.atomic
    def update_booking(pk: int, validated_data: Dict[str, Any]):
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return None

        old_status = booking.status
        old_qty = booking.quantity
        old_ticket = booking.ticket

        # Apply updates
        if 'customer' in validated_data:
            booking.customer = BookingService._resolve_fk(validated_data.get('customer'), Customer)
        if 'event' in validated_data:
            booking.event = BookingService._resolve_fk(validated_data.get('event'), Event)
        if 'ticket' in validated_data:
            booking.ticket = BookingService._resolve_fk(validated_data.get('ticket'), Ticket)
        if 'quantity' in validated_data:
            booking.quantity = validated_data.get('quantity')
        if 'total_amount' in validated_data:
            booking.total_amount = validated_data.get('total_amount')
        if 'status' in validated_data:
            booking.status = validated_data.get('status')

        booking.save()

        # ---------------------------------------------------------
        # Handle Ticket Sold Adjustments based on Status Transitions
        # ---------------------------------------------------------
        new_status = booking.status
        new_qty = booking.quantity
        new_ticket = booking.ticket

        if old_ticket and old_ticket == new_ticket:
            ticket = old_ticket
            # Ensure we have the latest stock data
            ticket.refresh_from_db()
            
            if old_status != 'confirmed' and new_status == 'confirmed':
                ticket.sold += new_qty
                ticket.save()
            elif old_status == 'confirmed' and new_status != 'confirmed':
                ticket.sold = max(0, ticket.sold - old_qty)
                ticket.save()
            elif old_status == 'confirmed' and new_status == 'confirmed':
                if old_qty != new_qty:
                    delta = new_qty - old_qty
                    ticket.sold = max(0, ticket.sold + delta)
                    ticket.save()
        elif old_ticket != new_ticket:
            # Ticket type changed: Handle stock for both old and new tickets
            if old_status == 'confirmed' and old_ticket:
                old_ticket.refresh_from_db()
                old_ticket.sold = max(0, old_ticket.sold - old_qty)
                old_ticket.save()
            if new_status == 'confirmed' and new_ticket:
                new_ticket.refresh_from_db()
                new_ticket.sold += new_qty
                new_ticket.save()

        return booking

    @staticmethod
    @transaction.atomic
    def delete_booking(pk: int):
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return False
        
        # Soft delete
        booking.is_deleted = True
        booking.deleted_at = timezone.now()
        booking.save()
        
        # Rollback ticket sold count ONLY if it was confirmed
        if booking.status == 'confirmed' and booking.ticket:
            ticket = booking.ticket
            ticket.refresh_from_db()
            ticket.sold = max(0, ticket.sold - booking.quantity)
            ticket.save()
            
        return True

    @staticmethod
    @transaction.atomic
    def force_delete_booking(pk: int):
        """
        Permanently delete a booking from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            # Use all_objects to find even soft-deleted items
            booking = Booking.all_objects.get(pk=pk)
            
            # Rollback ticket sold count if it was confirmed AND it wasn't already soft-deleted
            # (If it was soft-deleted, stock was already rolled back in delete_booking)
            if not booking.is_deleted and booking.status == 'confirmed' and booking.ticket:
                ticket = booking.ticket
                ticket.refresh_from_db()
                ticket.sold = max(0, ticket.sold - booking.quantity)
                ticket.save()
                
            booking.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    @transaction.atomic
    def restore_booking(pk: int):
        """
        Restore a soft-deleted booking.
        """
        try:
            # Use all_objects to find items that are currently soft-deleted
            booking = Booking.all_objects.get(pk=pk, is_deleted=True)
            
            # Restore booking
            booking.is_deleted = False
            booking.deleted_at = None
            booking.save()
            
            # Restore ticket sold count ONLY if it was confirmed
            if booking.status == 'confirmed' and booking.ticket:
                ticket = booking.ticket
                ticket.refresh_from_db()
                ticket.sold += booking.quantity
                ticket.save()
                
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_bookings(params: Dict[str, Any]):
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = Booking.all_objects.select_related('customer', 'event', 'ticket').filter(is_deleted=params.get('is_deleted', False))

        if search:
            qs = qs.filter(
                Q(customer__email__icontains=search) | Q(event__event_name__icontains=search) | Q(ticket__ticket_type__icontains=search)
            )

        if 'customer_id' in filters:
            qs = qs.filter(customer_id=filters['customer_id'])
        if 'event_id' in filters:
            qs = qs.filter(event_id=filters['event_id'])
        if 'ticket_id' in filters:
            qs = qs.filter(ticket_id=filters['ticket_id'])
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])

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