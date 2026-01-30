from django.urls import path
from app.views.role_views import RoleListCreateView, RoleRetrieveUpdateDestroyView, PaginatedRoleListView

urlpatterns = [
    path('', RoleListCreateView.as_view(), name='role-list-create'),
    path('<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-retrieve-update-destroy'),
    path('paginated/', PaginatedRoleListView.as_view(), name='paginated-role-list'),
]
