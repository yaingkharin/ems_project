from django.urls import path
from app.views.role_permission_views import RolePermissionListCreateView, RolePermissionRetrieveUpdateDestroyView, RolePermissionsListView, PaginatedRolePermissionListView

urlpatterns = [
    path('', RolePermissionListCreateView.as_view(), name='role-permission-list-create'),
    path('<int:pk>/', RolePermissionRetrieveUpdateDestroyView.as_view(), name='role-permission-retrieve-destroy'),
    path('paginated/', PaginatedRolePermissionListView.as_view(), name='paginated-role-permissions'),
]
