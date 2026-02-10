from typing import Dict, Any
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket


class BookingService:
    @staticmethod
    def _resolve_fk(value, model):
        if value is None:
            return None
        if isinstance(value, model):
            return value
        return model.objects.get(pk=value)

    @staticmethod
    def get_all_bookings():
        return Booking.objects.select_related('user', 'event', 'ticket').all()

    @staticmethod
    def get_booking_by_id(pk: int):
        try:
            return Booking.objects.select_related('user', 'event', 'ticket').get(pk=pk)
        except Booking.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_booking(validated_data: Dict[str, Any]):
        user = BookingService._resolve_fk(validated_data.get('user'), User)
        event = BookingService._resolve_fk(validated_data.get('event'), Event)
        ticket = BookingService._resolve_fk(validated_data.get('ticket'), Ticket)

        quantity = validated_data.get('quantity')
        total_amount = validated_data.get('total_amount')

        # Basic ticket availability check
        if ticket and quantity and ticket.quantity - ticket.sold < quantity:
            raise ValueError('Not enough tickets available')

        booking = Booking.objects.create(
            user=user,
            event=event,
            ticket=ticket,
            quantity=quantity,
            total_amount=total_amount,
            status=validated_data.get('status', 'pending')
        )

        # Update ticket sold count
        if ticket and quantity:
            ticket.sold += quantity
            ticket.save()

        return booking

    @staticmethod
    @transaction.atomic
    def update_booking(pk: int, validated_data: Dict[str, Any]):
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return None

        if 'user' in validated_data:
            booking.user = BookingService._resolve_fk(validated_data.get('user'), User)
        if 'event' in validated_data:
            booking.event = BookingService._resolve_fk(validated_data.get('event'), Event)
        if 'ticket' in validated_data:
            booking.ticket = BookingService._resolve_fk(validated_data.get('ticket'), Ticket)
        if 'quantity' in validated_data:
            # Adjust ticket sold counts if ticket is set
            old_qty = booking.quantity
            new_qty = validated_data.get('quantity')
            booking.quantity = new_qty
            if booking.ticket:
                delta = new_qty - old_qty
                booking.ticket.sold = max(0, booking.ticket.sold + delta)
                booking.ticket.save()
        if 'total_amount' in validated_data:
            booking.total_amount = validated_data.get('total_amount')
        if 'status' in validated_data:
            booking.status = validated_data.get('status')

        booking.save()
        return booking

    @staticmethod
    @transaction.atomic
    def delete_booking(pk: int):
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return False
        # Rollback ticket sold count
        if booking.ticket:
            booking.ticket.sold = max(0, booking.ticket.sold - booking.quantity)
            booking.ticket.save()
        booking.delete()
        return True

    @staticmethod
    def get_paginated_bookings(params: Dict[str, Any]):
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = Booking.objects.select_related('user', 'event', 'ticket').all()

        if search:
            qs = qs.filter(
                Q(user__email__icontains=search) | Q(event__event_name__icontains=search) | Q(ticket__ticket_type__icontains=search)
            )

        if 'user_id' in filters:
            qs = qs.filter(user_id=filters['user_id'])
        if 'event_id' in filters:
            qs = qs.filter(event_id=filters['event_id'])
        if 'ticket_id' in filters:
            qs = qs.filter(ticket_id=filters['ticket_id'])

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