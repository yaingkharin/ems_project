import datetime
from django.db.models import Sum, Count, Q
from django.utils import timezone
from app.models.booking import Booking
from app.models.event import Event
from app.models.customer import Customer
from app.models.ticket import Ticket
from app.models.event_ticket import EventTicket
from app.models.checkin import Checkin

class DashboardService:
    """
    Service layer for dashboard-specific data aggregation.
    """
    @staticmethod
    def get_dashboard_stats():
        today = timezone.now()
        last_week = today - datetime.timedelta(days=7)
        two_weeks_ago = today - datetime.timedelta(days=14)

        def get_trend(current_count, previous_count):
            if previous_count == 0:
                return 100.0 if current_count > 0 else 0.0
            return round(((current_count - previous_count) / previous_count) * 100, 1)

        # --- 1. Summary Stats ---
        # Revenue (Confirmed + Paid only)
        # Consistent with ReportService logic
        confirmed_paid_bookings = Booking.objects.filter(
            is_deleted=False, 
            status='confirmed',
            payments__status='completed',
            payments__is_deleted=False
        )

        total_revenue = confirmed_paid_bookings.aggregate(total=Sum('total_amount'))['total'] or 0
        
        prev_week_revenue = confirmed_paid_bookings.filter(
            created_at__lt=last_week, 
            created_at__gte=two_weeks_ago
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        curr_week_revenue = confirmed_paid_bookings.filter(
            created_at__gte=last_week
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        revenue_trend = get_trend(curr_week_revenue, prev_week_revenue)

        # Events
        total_events = Event.objects.filter(is_deleted=False).count()
        prev_events = Event.objects.filter(is_deleted=False, created_at__lt=last_week, created_at__gte=two_weeks_ago).count()
        curr_week_events = Event.objects.filter(is_deleted=False, created_at__gte=last_week).count()
        events_trend = get_trend(curr_week_events, prev_events)

        # Bookings (All non-deleted)
        total_bookings = Booking.objects.filter(is_deleted=False).count()
        prev_bookings = Booking.objects.filter(is_deleted=False, created_at__lt=last_week, created_at__gte=two_weeks_ago).count()
        curr_week_bookings = Booking.objects.filter(is_deleted=False, created_at__gte=last_week).count()
        bookings_trend = get_trend(curr_week_bookings, prev_bookings)

        # Customers
        total_customers = Customer.objects.filter(is_deleted=False).count()
        prev_customers = Customer.objects.filter(is_deleted=False, created_at__lt=last_week, created_at__gte=two_weeks_ago).count()
        curr_week_customers = Customer.objects.filter(is_deleted=False, created_at__gte=last_week).count()
        customers_trend = get_trend(curr_week_customers, prev_customers)

        # --- 2. Ticket Metrics ---
        # Inventory capacity (Total slots available)
        total_tickets_capacity = Ticket.objects.filter(is_deleted=False).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Tickets Sold (Confirmed bookings)
        tickets_sold = confirmed_paid_bookings.aggregate(total=Sum('quantity'))['total'] or 0
        
        # Tickets Generated (Actual unique ticket records/QR codes created)
        tickets_generated_count = EventTicket.objects.filter(is_deleted=False).count()
        
        # Tickets Confirmed (Tickets marked as USED or checked-in)
        total_checked_in = EventTicket.objects.filter(status='USED', is_deleted=False).count()
        
        prev_checked_in = Checkin.objects.filter(status='SUCCESS', is_deleted=False, created_at__lt=last_week, created_at__gte=two_weeks_ago).count()
        curr_checked_in = Checkin.objects.filter(status='SUCCESS', is_deleted=False, created_at__gte=last_week).count()
        checked_in_trend = get_trend(curr_checked_in, prev_checked_in)

        # --- 3. Charts Data (Last 7 Days) ---
        revenue_trend_data = []
        bookings_per_day_data = []
        labels = []
        for i in range(6, -1, -1):
            day = today - datetime.timedelta(days=i)
            day_str = day.strftime("%d %b")
            labels.append(day_str)
            
            # Using range is more reliable than __date across different DB timezones
            start_of_day = timezone.make_aware(datetime.datetime.combine(day.date(), datetime.time.min))
            end_of_day = timezone.make_aware(datetime.datetime.combine(day.date(), datetime.time.max))
            
            day_rev = confirmed_paid_bookings.filter(
                created_at__range=(start_of_day, end_of_day)
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            revenue_trend_data.append(float(day_rev))
            
            day_bookings = Booking.objects.filter(
                is_deleted=False,
                created_at__range=(start_of_day, end_of_day)
            ).count()
            bookings_per_day_data.append(day_bookings)

        # --- 4. Pending Bookings Today ---
        # Re-using the today range calculated for charts
        today_start = timezone.make_aware(datetime.datetime.combine(today.date(), datetime.time.min))
        today_end = timezone.make_aware(datetime.datetime.combine(today.date(), datetime.time.max))
        
        pending_bookings = Booking.objects.filter(
            status='pending',
            created_at__range=(today_start, today_end)
        ).select_related('customer', 'event', 'ticket').order_by('-created_at')[:5]
        
        # --- 5. Top 5 Events ---
        top_events = Event.objects.filter(is_deleted=False).annotate(
            revenue=Sum('bookings__total_amount', filter=Q(bookings__status='confirmed', bookings__is_deleted=False)),
            bookings_count=Count('bookings', distinct=True, filter=Q(bookings__is_deleted=False)),
            tickets_sold_sum=Sum('bookings__quantity', filter=Q(bookings__status='confirmed', bookings__is_deleted=False))
        ).order_by('-revenue')[:5]

        # --- 6. Status Distribution ---
        status_dist = Booking.objects.filter(is_deleted=False).values('status').annotate(count=Count('id'))
        status_map = {item['status']: item['count'] for item in status_dist}
        status_map['checked_in'] = total_checked_in

        return {
            "summary": {
                "total_revenue": {"value": float(total_revenue), "trend": revenue_trend},
                "total_events": {"value": total_events, "trend": events_trend},
                "total_bookings": {"value": total_bookings, "trend": bookings_trend},
                "total_customers": {"value": total_customers, "trend": customers_trend},
                "total_tickets": {"value": total_tickets_capacity, "trend": 0},
                "tickets_sold": {"value": tickets_sold, "trend": 0},
                "tickets_generated": {"value": tickets_generated_count, "trend": 0},
                "tickets_confirmed": {"value": total_checked_in, "trend": checked_in_trend}
            },
            "charts": {
                "revenue_trend": {"labels": labels, "data": revenue_trend_data},
                "bookings_per_day": {"labels": labels, "data": bookings_per_day_data},
                "status_distribution": [
                    {"label": "Confirmed", "value": status_map.get('confirmed', 0), "color": "#10b981"},
                    {"label": "Pending", "value": status_map.get('pending', 0), "color": "#f59e0b"},
                    {"label": "Cancelled", "value": status_map.get('cancelled', 0), "color": "#ef4444"},
                    {"label": "Checked-in", "value": status_map.get('checked_in', 0), "color": "#3b82f6"}
                ]
            },
            "pending_bookings": [
                {
                    "id": b.id,
                    "customer_name": f"{b.customer.first_name} {b.customer.last_name}",
                    "event_name": b.event.event_name,
                    "ticket_qty": b.quantity,
                    "amount": float(b.total_amount),
                    "booking_time": b.created_at.strftime("%I:%M %p"),
                    "status": b.status
                } for b in pending_bookings
            ],
            "top_events": [
                {
                    "name": e.event_name,
                    "revenue": float(e.revenue or 0),
                    "bookings": e.bookings_count,
                    "tickets_sold": e.tickets_sold_sum or 0
                } for e in top_events
            ]
        }
