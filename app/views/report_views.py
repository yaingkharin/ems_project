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

