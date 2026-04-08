from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from app.models.checkin import Checkin
from app.models.booking import Booking
from app.models.event_ticket import EventTicket
from app.dto.responses.checkin_response import CheckinResponse


class CheckinService:
    """
    Service layer for handling check-in related business logic.
    """

    @staticmethod
    def create_checkin(request_data: dict) -> Checkin:
        """
        Creates a new check-in.
        """
        booking_id = request_data.pop('booking_id', None)
        booking = Booking.objects.get(id=booking_id) if booking_id else None
        checkin = Checkin.objects.create(
            booking=booking,
            **request_data
        )
        return checkin

    @staticmethod
    def validate_ticket(ticket_code: str) -> dict:
        """
        Validates an event ticket by its code.
        Returns the details necessary for the check-in UI and logs invalid attempts if necessary.
        """
        try:
            ticket = EventTicket.objects.select_related('booking__customer', 'booking__event', 'booking__ticket').get(ticket_code=ticket_code)
            booking = ticket.booking
            customer_name = f"{booking.customer.first_name} {booking.customer.last_name}" if booking and booking.customer else "Unknown"
            event_name = booking.event.event_name if booking and booking.event else "Unknown"
            ticket_type = booking.ticket.ticket_name if booking and booking.ticket else "-"
            booking_id_val = booking.id if booking else None
            
            status = 'VALID' if ticket.status == 'UNUSED' else 'ALREADY_USED'

            return {
                "ticket_code": ticket_code,
                "customer_name": customer_name,
                "event_name": event_name,
                "ticket_type": ticket_type,
                "booking_id": booking_id_val,
                "status": status
            }
        except ObjectDoesNotExist:
            return {
                "ticket_code": ticket_code,
                "customer_name": "Unknown",
                "event_name": "Unknown",
                "ticket_type": "-",
                "booking_id": None,
                "status": "INVALID"
            }

    @staticmethod
    def confirm_checkin(ticket_code: str) -> dict:
        """
        Confirms a check-in by updating the event ticket status and logging the attempt.
        """
        try:
            ticket = EventTicket.objects.get(ticket_code=ticket_code)
            
            if ticket.status == 'USED':
                Checkin.objects.create(ticket_code=ticket_code, booking=ticket.booking, status='ALREADY_USED')
                return {"success": False, "message": "Ticket is already used."}
            
            # Update ticket status
            ticket.status = 'USED'
            ticket.save()
            
            # Log successful check-in
            Checkin.objects.create(ticket_code=ticket_code, booking=ticket.booking, status='SUCCESS')
            
            return {"success": True, "message": "Check-in successful."}
        except ObjectDoesNotExist:
            # Log invalid check-in attempt
            Checkin.objects.create(ticket_code=ticket_code, booking=None, status='INVALID')
            return {"success": False, "message": "Invalid ticket code."}

    @staticmethod
    def get_checkin_by_id(checkin_id: int) -> Optional[Checkin]:
        """
        Retrieves a single check-in by its ID.
        """
        try:
            return Checkin.objects.select_related('booking').get(id=checkin_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_checkins() -> List[Checkin]:
        """
        Retrieves all check-ins.
        """
        return Checkin.objects.select_related('booking').filter(is_deleted=False)

    @staticmethod
    def update_checkin(checkin_id: int, request_data: dict) -> Optional[Checkin]:
        """
        Updates an existing check-in.
        """
        try:
            checkin = Checkin.objects.get(id=checkin_id, is_deleted=False)

            if 'booking_id' in request_data:
                checkin.booking = Booking.objects.get(id=request_data.pop('booking_id'))

            for key, value in request_data.items():
                setattr(checkin, key, value)

            checkin.save()
            return checkin
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_checkin(checkin_id: int) -> bool:
        """
        Soft deletes a check-in by its ID.
        """
        try:
            checkin = Checkin.objects.get(id=checkin_id)
            checkin.is_deleted = True
            checkin.deleted_at = timezone.now()
            checkin.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_checkin(checkin_id: int) -> bool:
        """
        Permanently delete a check-in from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            checkin = Checkin.objects.get(id=checkin_id)
            checkin.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_checkins(validated_data: dict) -> dict:
        """
        Retrieves a paginated list of check-ins with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 10)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Checkin.objects.select_related('booking').filter(is_deleted=False)

        if filters:
            queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(ticket_code__icontains=search) |
                Q(status__icontains=search) |
                Q(booking__id__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_checkins = paginator.page(page)
        except PageNotAnInteger:
            paginated_checkins = paginator.page(1)
        except EmptyPage:
            paginated_checkins = paginator.page(paginator.num_pages)

        checkins_data = CheckinResponse(paginated_checkins.object_list, many=True).data

        return {
            'data': checkins_data,
            'total': paginator.count,
            'page': paginated_checkins.number,
            'limit': limit,
        }
