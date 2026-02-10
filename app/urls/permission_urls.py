from django.urls import path
from app.views.permission_views import PermissionListCreateView, PermissionRetrieveUpdateDestroyView, PaginatedPermissionListView

urlpatterns = [
    path('', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('<int:pk>/', PermissionRetrieveUpdateDestroyView.as_view(), name='permission-retrieve-update-destroy'),
    path('paginated/', PaginatedPermissionListView.as_view(), name='paginated-permission-list'),
]
