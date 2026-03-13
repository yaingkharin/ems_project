from typing import Dict, Any
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event


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
        return Booking.objects.select_related('customer', 'event').all()

    @staticmethod
    def get_booking_by_id(pk: int):
        try:
            return Booking.objects.select_related('customer', 'event').get(pk=pk)
        except Booking.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_booking(validated_data: Dict[str, Any]):
        customer = BookingService._resolve_fk(validated_data.get('customer'), User)
        event = BookingService._resolve_fk(validated_data.get('event'), Event)

        quantity = validated_data.get('quantity')
        total_amount = validated_data.get('total_amount')

        booking = Booking.objects.create(
            customer=customer,
            event=event,
            quantity=quantity,
            total_amount=total_amount,
            status=validated_data.get('status', 'pending')
        )

        return booking

    @staticmethod
    @transaction.atomic
    def update_booking(pk: int, validated_data: Dict[str, Any]):
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return None

        if 'customer' in validated_data:
            booking.customer = BookingService._resolve_fk(validated_data.get('customer'), User)
        if 'event' in validated_data:
            booking.event = BookingService._resolve_fk(validated_data.get('event'), Event)
        if 'quantity' in validated_data:
            booking.quantity = validated_data.get('quantity')
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
        # Soft delete instead of hard delete
        booking.is_deleted = True
        booking.deleted_at = timezone.now()
        booking.save()
        return True

    @staticmethod
    @transaction.atomic
    def force_delete_booking(pk: int):
        """
        Permanently delete a booking from the database.
        Use with caution - this action cannot be undone.
        """
        booking = BookingService.get_booking_by_id(pk)
        if not booking:
            return False
        booking.delete()  # Hard delete
        return True

    @staticmethod
    def get_paginated_bookings(params: Dict[str, Any]):
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = Booking.objects.select_related('customer', 'event').all()

        if search:
            qs = qs.filter(
                Q(customer__email__icontains=search) | Q(event__event_name__icontains=search)
            )

        if 'customer_id' in filters:
            qs = qs.filter(customer_id=filters['customer_id'])
        if 'event_id' in filters:
            qs = qs.filter(event_id=filters['event_id'])

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