import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.services.dashboard_service import DashboardService

def test_dashboard_api():
    try:
        stats = DashboardService.get_dashboard_stats()
        print(json.dumps(stats, indent=2))
        print("\nSuccess: Dashboard statistics generated successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_dashboard_api()
