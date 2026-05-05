from django.urls import path
from app.views.report_views import (
    BookingReportView, 
    RevenueReportView, 
    PaymentMethodReportView, 
    AttendanceReportView,
    EventBookingReportView,
    CheckInReportView,
    TicketReportView
)

urlpatterns = [
    path('booking-report/', BookingReportView.as_view(), name='booking_report'),
    path('revenue/', RevenueReportView.as_view(), name='report_revenue'),
    path('payment-methods/', PaymentMethodReportView.as_view(), name='report_payment_methods'),
    path('attendance/', AttendanceReportView.as_view(), name='report_attendance'),
    path('event-report-list/', EventBookingReportView.as_view(), name='event_report_list'),
    path('check-in-report/', CheckInReportView.as_view(), name='check_in_report'),
    path('tickets/', TicketReportView.as_view(), name='report_tickets'),
]

