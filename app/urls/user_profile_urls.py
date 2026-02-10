from django.urls import path
from app.views.user_profile_views import UserProfileListCreateView, UserProfileRetrieveUpdateDestroyView, PaginatedUserProfileListView

urlpatterns = [
    path('', UserProfileListCreateView.as_view(), name='user-profile-list-create'),
    path('<int:pk>/', UserProfileRetrieveUpdateDestroyView.as_view(), name='user-profile-retrieve-update-destroy'),
    path('paginate/', PaginatedUserProfileListView.as_view(), name='user-profile-paginate'),
]