from django.urls import path
from app.views.report_views import (
    BookingReportView, 
    RevenueReportView, 
    PaymentMethodReportView, 
    AttendanceReportView
)

urlpatterns = [
    path('booking-report/', BookingReportView.as_view(), name='booking_report'),
    path('revenue/', RevenueReportView.as_view(), name='report_revenue'),
    path('payment-methods/', PaymentMethodReportView.as_view(), name='report_payment_methods'),
    path('attendance/', AttendanceReportView.as_view(), name='report_attendance'),
]

