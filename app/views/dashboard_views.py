from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from app.services.dashboard_service import DashboardService
from app.utils.api_response import api_response
from app.utils.permissions import CheckPermission

class DashboardStatsView(APIView):
    """
    Dashboard API for retrieving administrative statistics and charts data.
    """
    permission_classes = [IsAuthenticated, CheckPermission]
    method_permissions = {
        'GET': 'view_dashboard', # Assuming 'view_dashboard' is a valid permission string
    }

    @swagger_auto_schema(
        operation_description="Retrieve dashboard summary statistics, chart data, pending bookings, and top events.",
        responses={200: "Dashboard statistics JSON"}
    )
    def get(self, request):
        try:
            stats = DashboardService.get_dashboard_stats()
            return api_response(data=stats, message="Dashboard statistics retrieved successfully.")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Dashboard error: {str(e)}")
            return api_response(message=f"Failed to retrieve dashboard stats: {str(e)}", success=False, status_code=500)
