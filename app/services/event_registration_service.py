from typing import Dict, Any
from django.db import transaction, IntegrityError
from django.db.models import Q
from app.models.event_registration import EventRegistration
from app.models.user import User
from app.models.event import Event


class EventRegistrationService:
    @staticmethod
    def _resolve_fk(value, model):
        if value is None:
            return None
        if isinstance(value, model):
            return value
        return model.objects.get(pk=value)

    @staticmethod
    def get_all_event_registrations():
        return EventRegistration.objects.select_related('user', 'event').all()

    @staticmethod
    def get_event_registration_by_id(pk: int):
        try:
            return EventRegistration.objects.select_related('user', 'event').get(pk=pk)
        except EventRegistration.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_event_registration(validated_data: Dict[str, Any]):
        user = EventRegistrationService._resolve_fk(validated_data.get('user'), User)
        event = EventRegistrationService._resolve_fk(validated_data.get('event'), Event)

        try:
            registration = EventRegistration.objects.create(
                user=user,
                event=event,
                status=validated_data.get('status', 'pending')
            )
        except IntegrityError as exc:
            # Unique constraint (user,event) may already exist
            raise ValueError('User already registered for this event') from exc

        return registration

    @staticmethod
    @transaction.atomic
    def update_event_registration(pk: int, validated_data: Dict[str, Any]):
        reg = EventRegistrationService.get_event_registration_by_id(pk)
        if not reg:
            return None

        if 'user' in validated_data:
            reg.user = EventRegistrationService._resolve_fk(validated_data.get('user'), User)
        if 'event' in validated_data:
            reg.event = EventRegistrationService._resolve_fk(validated_data.get('event'), Event)
        if 'status' in validated_data:
            reg.status = validated_data.get('status')

        reg.save()
        return reg

    @staticmethod
    @transaction.atomic
    def delete_event_registration(pk: int):
        reg = EventRegistrationService.get_event_registration_by_id(pk)
        if not reg:
            return False
        reg.delete()
        return True

    @staticmethod
    def get_paginated_event_registrations(params: Dict[str, Any]):
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')
        search = params.get('search')
        filters = params.get('filters') or {}

        qs = EventRegistration.objects.select_related('user', 'event').all()

        if search:
            qs = qs.filter(
                Q(user__email__icontains=search) | Q(event__event_name__icontains=search)
            )

        if 'user_id' in filters:
            qs = qs.filter(user_id=filters['user_id'])
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