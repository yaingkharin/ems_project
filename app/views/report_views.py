from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.services.report_service import ReportService
from app.dto.requests.pagination_request import PaginationRequest
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission

class BookingReportView(APIView):
    """
    Provides a comprehensive report for bookings, including related event, ticket, and payment info.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'POST': 'view_reports', # Using 'view_reports' as the required permission
    }

    @swagger_auto_schema(
        operation_description="Retrieve a paginated, searchable, and filterable booking report.",
        request_body=PaginationRequest,
        responses={
            200: openapi.Response(
                description="List of booking report items.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "items": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "limit": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "total_pages": openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        try:
            report_data = ReportService.get_booking_report(params)
            return api_response(
                data=report_data,
                message="Booking report retrieved successfully."
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=400
            )

class RevenueReportView(APIView):
    """
    Provides a revenue summary report aggregated by event.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {'POST': 'view_reports'}

    @swagger_auto_schema(
        operation_description="Retrieve a paginated revenue summary report.",
        request_body=PaginationRequest,
        responses={200: "Success"}
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            report_data = ReportService.get_revenue_report(serializer.validated_data)
            return api_response(data=report_data, message="Revenue report retrieved successfully.")
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=400)

class PaymentMethodReportView(APIView):
    """
    Provides a report on total transactions and amount collected by each payment method.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {'POST': 'view_reports'}

    @swagger_auto_schema(
        operation_description="Retrieve a paginated payment method report.",
        request_body=PaginationRequest,
        responses={200: "Success"}
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            report_data = ReportService.get_payment_method_report(serializer.validated_data)
            return api_response(data=report_data, message="Payment method report retrieved successfully.")
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=400)

class AttendanceReportView(APIView):
    """
    Provides an attendance versus booking report per event.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {'POST': 'view_reports'}

    @swagger_auto_schema(
        operation_description="Retrieve a paginated attendance report.",
        request_body=PaginationRequest,
        responses={200: "Success"}
    )
    def post(self, request):
        serializer = PaginationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            report_data = ReportService.get_attendance_report(serializer.validated_data)
            return api_response(data=report_data, message="Attendance report retrieved successfully.")
        except Exception as e:
            return api_response(message=str(e), success=False, status_code=400)

from rest_framework import generics
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
import csv
import openpyxl
from app.models.booking import Booking
from app.models.event import Event
from app.models.event_ticket import EventTicket
from app.dto.responses.report_response import EventBookingReportItemSerializer, CheckInReportItemSerializer
from django.utils import timezone
from datetime import datetime, time

class EventBookingReportView(generics.ListAPIView):
    """
    ListAPIView for Event Booking & Payment Report with filtering, aggregation, and exports.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {'GET': 'view_reports'}
    serializer_class = EventBookingReportItemSerializer

    @swagger_auto_schema(
        operation_description="Retrieve Event Booking & Payment Report with optional filtering.",
        manual_parameters=[
            openapi.Parameter('event_id', openapi.IN_QUERY, description="Filter by Event ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by payment status ('confirmed' or 'unconfirmed')", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by booking date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search across customer name, email, event name, or booking ID", type=openapi.TYPE_STRING),
            openapi.Parameter('export', openapi.IN_QUERY, description="Export format ('excel' or 'csv')", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Booking.objects.select_related('customer', 'event').prefetch_related('payments')
        
        # 1. Select Event Filter
        event_id = self.request.query_params.get('event_id')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
            
        # 2. Date Filter
        date_str = self.request.query_params.get('date')
        if date_str:
            try:
                # Parse date string (expecting YYYY-MM-DD)
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                # Create aware start and end of day in the current timezone
                tz = timezone.get_current_timezone()
                start_of_day = timezone.make_aware(datetime.combine(target_date, time.min), tz)
                end_of_day = timezone.make_aware(datetime.combine(target_date, time.max), tz)
                
                queryset = queryset.filter(booking_date__range=(start_of_day, end_of_day))
            except (ValueError, TypeError):
                # If date format is invalid, we can either ignore it or return empty
                pass
            
        # 3. Search Filter
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(customer__first_name__icontains=search_query) |
                Q(customer__last_name__icontains=search_query) |
                Q(customer__email__icontains=search_query) |
                Q(event__event_name__icontains=search_query) |
                Q(id__icontains=search_query)
            )
            
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        # Base queryset with all filters EXCEPT status
        base_queryset = self.filter_queryset(self.get_queryset())

        # Aggregation from base_queryset
        total_bookings = base_queryset.count()
        confirmed_count = base_queryset.filter(payments__status='completed').distinct().count()
        unconfirmed_count = total_bookings - confirmed_count
        
        # Calculate revenue only for confirmed payments from base_queryset
        total_revenue = base_queryset.filter(payments__status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Now apply Status Buttons Filter to the items list
        queryset = base_queryset
        status = request.query_params.get('status')
        if status == 'confirmed':
            queryset = queryset.filter(payments__status='completed')
        elif status == 'unconfirmed':
            queryset = queryset.exclude(payments__status='completed')

        # Check for exports
        export = request.query_params.get('export')
        if export == 'excel':
            return self.export_excel(queryset)
        elif export == 'csv':
            return self.export_csv(queryset)

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Add summary to paginated response
            paginated_response.data['summary'] = {
                'total_bookings': total_bookings,
                'confirmed_count': confirmed_count,
                'unconfirmed_count': unconfirmed_count,
                'total_revenue': total_revenue
            }
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data={
                'summary': {
                    'total_bookings': total_bookings,
                    'confirmed_count': confirmed_count,
                    'unconfirmed_count': unconfirmed_count,
                    'total_revenue': float(total_revenue)
                },
                'items': serializer.data
            },
            message="Event booking report retrieved successfully."
        )

    def export_excel(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Event Booking Report"

        headers = ['Booking ID', 'Event Name', 'Customer Name', 'Username', 'Booking Date', 'Quantity', 'Total Amount', 'Payment Method', 'Status']
        ws.append(headers)

        for item in data:
            ws.append([
                item['booking_id'], item['event_name'], item['customer_name'], 
                item['username'], item['booking_date'], item['quantity'], 
                item['total_amount'], item['payment_method'], item['status']
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=event_booking_report.xlsx'
        wb.save(response)
        return response

    def export_csv(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=event_booking_report.csv'

        writer = csv.writer(response)
        headers = ['Booking ID', 'Event Name', 'Customer Name', 'Username', 'Booking Date', 'Quantity', 'Total Amount', 'Payment Method', 'Status']
        writer.writerow(headers)

        for item in data:
            writer.writerow([
                item['booking_id'], item['event_name'], item['customer_name'], 
                item['username'], item['booking_date'], item['quantity'], 
                item['total_amount'], item['payment_method'], item['status']
            ])

        return response


class CheckInReportView(generics.ListAPIView):
    """
    ListAPIView for Event Check-in Report with filtering, aggregation, and exports.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {'GET': 'view_reports'}
    serializer_class = CheckInReportItemSerializer

    @swagger_auto_schema(
        operation_description="Retrieve Event Check-in Report with optional filtering.",
        manual_parameters=[
            openapi.Parameter('event_id', openapi.IN_QUERY, description="Filter by Event ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by check-in status ('checked_in' or 'not_checked_in')", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by Event Date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by Event Name, Ticket Code, or Customer Name", type=openapi.TYPE_STRING),
            openapi.Parameter('export', openapi.IN_QUERY, description="Export format ('excel' or 'csv')", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = EventTicket.objects.select_related('booking__customer', 'booking__event').filter(is_deleted=False)
        
        # 1. Event Filter
        event_id = self.request.query_params.get('event_id')
        if event_id:
            queryset = queryset.filter(booking__event_id=event_id)
            
        # 2. Date Filter
        date_str = self.request.query_params.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(booking__booking_date__date=target_date)
            except (ValueError, TypeError):
                pass
            
        # 3. Search Filter
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(booking__event__event_name__icontains=search_query) |
                Q(ticket_code__icontains=search_query) |
                Q(booking__customer__first_name__icontains=search_query) |
                Q(booking__customer__last_name__icontains=search_query) |
                Q(booking__customer__email__icontains=search_query)
            )
            
        return queryset

    def list(self, request, *args, **kwargs):
        base_queryset = self.filter_queryset(self.get_queryset())

        # Summary statistics from the base filtered queryset
        total_tickets = base_queryset.count()
        checked_in_count = base_queryset.filter(status='USED').count()
        not_checked_in_count = total_tickets - checked_in_count
        overall_rate = (checked_in_count / total_tickets * 100) if total_tickets > 0 else 0

        summary = {
            'total_tickets': total_tickets,
            'checked_in_count': checked_in_count,
            'not_checked_in_count': not_checked_in_count,
            'checkin_rate': round(overall_rate, 2)
        }

        # Apply Status Filter to the items list
        queryset = base_queryset
        status = request.query_params.get('status')
        if status == 'checked_in':
            queryset = queryset.filter(status='USED')
        elif status == 'not_checked_in':
            queryset = queryset.filter(status='UNUSED')

        # Check for exports
        export = request.query_params.get('export')
        if export == 'excel':
            return self.export_excel(queryset)
        elif export == 'csv':
            return self.export_csv(queryset)

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['summary'] = summary
            return paginated_response

        # Non-paginated
        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data={
                'summary': summary,
                'items': serializer.data
            },
            message="Event check-in report retrieved successfully."
        )

    def export_excel(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Check-in Report"

        headers = ['Ticket Code', 'Event Name', 'Customer Name', 'Username', 'Booking Date', 'Status']
        ws.append(headers)

        for item in data:
            ws.append([
                item['ticket_code'], item['event_name'], item['customer_name'], 
                item['username'], item['booking_date'], item['status']
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=checkin_report.xlsx'
        wb.save(response)
        return response

    def export_csv(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=checkin_report.csv'

        writer = csv.writer(response)
        headers = ['Ticket Code', 'Event Name', 'Customer Name', 'Username', 'Booking Date', 'Status']
        writer.writerow(headers)

        for item in data:
            writer.writerow([
                item['ticket_code'], item['event_name'], item['customer_name'], 
                item['username'], item['booking_date'], item['status']
            ])

        return response

