from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.ticket import Ticket
from app.models.event import Event
from app.dto.responses.ticket_response import TicketResponse

class TicketService:
    @staticmethod
    def create_ticket(request_data: dict) -> Ticket:
        event = Event.objects.get(id=request_data.pop('event_id'))
        ticket = Ticket.objects.create(
            event=event,
            **request_data
        )
        return ticket

    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Optional[Ticket]:
        try:
            return Ticket.objects.get(id=ticket_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_tickets() -> List[Ticket]:
        return Ticket.objects.all()

    @staticmethod
    def update_ticket(ticket_id: int, request_data: dict) -> Optional[Ticket]:
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if 'event_id' in request_data:
                ticket.event = Event.objects.get(id=request_data.pop('event_id'))
            
            for key, value in request_data.items():
                setattr(ticket, key, value)
            
            ticket.save()
            return ticket
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_ticket(ticket_id: int) -> bool:
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_tickets(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Ticket.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(ticket_type__icontains=search) |
                Q(event__event_name__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_tickets = paginator.page(page)
        except PageNotAnInteger:
            paginated_tickets = paginator.page(1)
        except EmptyPage:
            paginated_tickets = paginator.page(paginator.num_pages)

        tickets_data = TicketResponse(paginated_tickets.object_list, many=True).data

        return {
            'data': tickets_data,
            'total': paginator.count,
            'page': paginated_tickets.number,
            'limit': limit,
        }