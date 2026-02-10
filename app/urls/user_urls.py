from django.urls import path
from app.views.user_views import UserListCreateView, UserRetrieveUpdateDestroyView, PaginatedUserListView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('paginated/', PaginatedUserListView.as_view(), name='paginated-user-list'),
]
