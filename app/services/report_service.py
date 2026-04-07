from typing import Dict, Any, List
from django.db.models import Q, F, Sum, Count, ExpressionWrapper, FloatField
from django.utils import timezone
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.event import Event
from app.models.ticket import Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ReportService:
    @staticmethod
    def get_booking_report(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves a paginated, searchable, and filterable report of bookings,
        including related event, ticket, and payment information.
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        search = params.get('search')
        filters = params.get('filters', {})

        # Base queryset with essential joins
        queryset = Booking.objects.select_related('customer', 'event', 'ticket').filter(is_deleted=False)

        # ---------------------------------------------------------
        # Searching
        # ---------------------------------------------------------
        if search:
            queryset = queryset.filter(
                Q(customer__email__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(event__event_name__icontains=search) |
                Q(ticket__ticket_type__icontains=search)
            )

        # ---------------------------------------------------------
        # Filtering
        # ---------------------------------------------------------
        if 'event_id' in filters and filters['event_id']:
            queryset = queryset.filter(event_id=filters['event_id'])

        if 'status' in filters and filters['status']:
            queryset = queryset.filter(status=filters['status'])

        if 'start_date' in filters and filters['start_date']:
            queryset = queryset.filter(booking_date__gte=filters['start_date'])
        if 'end_date' in filters and filters['end_date']:
            queryset = queryset.filter(booking_date__lte=filters['end_date'])

        if 'payment_status' in filters and filters['payment_status']:
            queryset = queryset.filter(payments__status=filters['payment_status'])

        if 'payment_start_date' in filters and filters['payment_start_date']:
            queryset = queryset.filter(payments__paid_at__gte=filters['payment_start_date'])
        if 'payment_end_date' in filters and filters['payment_end_date']:
            queryset = queryset.filter(payments__paid_at__lte=filters['payment_end_date'])

        queryset = queryset.distinct().order_by('-booking_date')

        # ---------------------------------------------------------
        # Pagination
        # ---------------------------------------------------------
        paginator = Paginator(queryset, limit)
        try:
            paginated_qs = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_qs = paginator.page(1)

        report_data = []
        for booking in paginated_qs:
            payments = booking.payments.filter(is_deleted=False).values(
                'id', 'amount', 'status', 'payment_method', 'paid_at', 'currency'
            )
            
            report_data.append({
                'booking_id': booking.id,
                'booking_date': booking.booking_date,
                'status': booking.status,
                'total_amount': float(booking.total_amount),
                'quantity': booking.quantity,
                'customer': {
                    'id': booking.customer.id,
                    'email': booking.customer.email,
                    'full_name': f"{booking.customer.first_name} {booking.customer.last_name}".strip()
                },
                'event': {
                    'id': booking.event.id,
                    'name': booking.event.event_name
                },
                'ticket': {
                    'id': booking.ticket.id,
                    'type': booking.ticket.ticket_type,
                    'price': float(booking.ticket.price) if booking.ticket.price else 0
                },
                'payments': list(payments)
            })

        return {
            'items': report_data,
            'total': paginator.count,
            'page': paginated_qs.number,
            'limit': limit,
            'total_pages': paginator.num_pages
        }

    @staticmethod
    def get_revenue_report(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Revenue Summary Report: Aggregates revenue and ticket sales per event.
        Focuses on 'confirmed' bookings with 'completed' payments by default.
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        filters = params.get('filters', {})

        # Start with confirmed bookings and completed payments
        queryset = Booking.objects.filter(
            is_deleted=False, 
            status='confirmed',
            payments__status='completed',
            payments__is_deleted=False
        )

        if 'event_id' in filters and filters['event_id']:
            queryset = queryset.filter(event_id=filters['event_id'])
        if 'start_date' in filters and filters['start_date']:
            queryset = queryset.filter(event__event_date__gte=filters['start_date'])
        if 'end_date' in filters and filters['end_date']:
            queryset = queryset.filter(event__event_date__lte=filters['end_date'])

        # Aggregate data by event
        report_qs = queryset.values('event_id', 'event__event_name').annotate(
            total_revenue=Sum('total_amount'),
            total_tickets_sold=Sum('quantity'),
            total_bookings=Count('id', distinct=True)
        ).order_by('-total_revenue')

        paginator = Paginator(report_qs, limit)
        try:
            paginated_qs = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_qs = paginator.page(1)

        return {
            'items': list(paginated_qs),
            'total': paginator.count,
            'page': paginated_qs.number,
            'limit': limit,
            'total_pages': paginator.num_pages
        }

    @staticmethod
    def get_payment_method_report(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Payment Method Report: Breakdown of transactions by method.
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        filters = params.get('filters', {})

        queryset = Payment.objects.filter(status='completed', is_deleted=False)

        if 'start_date' in filters and filters['start_date']:
            queryset = queryset.filter(paid_at__gte=filters['start_date'])
        if 'end_date' in filters and filters['end_date']:
            queryset = queryset.filter(paid_at__lte=filters['end_date'])

        report_qs = queryset.values('payment_method').annotate(
            transaction_count=Count('id'),
            total_collected=Sum('amount')
        ).order_by('-total_collected')

        paginator = Paginator(report_qs, limit)
        try:
            paginated_qs = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_qs = paginator.page(1)

        return {
            'items': list(paginated_qs),
            'total': paginator.count,
            'page': paginated_qs.number,
            'limit': limit,
            'total_pages': paginator.num_pages
        }

    @staticmethod
    def get_attendance_report(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attendance Report: Comparison of tickets sold vs check-ins per event.
        """
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        filters = params.get('filters', {})

        # Start from Events to potentially show events with 0 sales/checkins if needed,
        # but here we join via bookings for sales data.
        queryset = Event.objects.filter(is_deleted=False)

        if 'event_id' in filters and filters['event_id']:
            queryset = queryset.filter(id=filters['event_id'])
        if 'start_date' in filters and filters['start_date']:
            queryset = queryset.filter(event_date__gte=filters['start_date'])
        if 'end_date' in filters and filters['end_date']:
            queryset = queryset.filter(event_date__lte=filters['end_date'])

        # Annotate sold vs checked in
        # Note: tickets_checked_in counts check-in records related to this event's bookings
        report_qs = queryset.annotate(
            tickets_sold=Sum('bookings__quantity'),
            tickets_checked_in=Count('bookings__checkins', filter=Q(bookings__checkins__status='checked_in', bookings__checkins__is_deleted=False))
        ).values('id', 'event_name', 'tickets_sold', 'tickets_checked_in')

        paginator = Paginator(report_qs, limit)
        try:
            paginated_qs = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_qs = paginator.page(1)

        # Calculate rate post-query to avoid complex SQL division/NULL handling
        report_data = []
        for item in paginated_qs:
            sold = item['tickets_sold'] or 0
            checked_in = item['tickets_checked_in'] or 0
            rate = (checked_in / sold * 100) if sold > 0 else 0
            item['attendance_rate'] = round(rate, 2)
            report_data.append(item)

        return {
            'items': report_data,
            'total': paginator.count,
            'page': paginated_qs.number,
            'limit': limit,
            'total_pages': paginator.num_pages
        }

