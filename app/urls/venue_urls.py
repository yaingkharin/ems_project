from django.urls import path
from app.views.venue_views import (
    VenueListCreateView,
    VenueRetrieveUpdateDestroyView,
    PaginatedVenueListView,
)

urlpatterns = [
    path('', VenueListCreateView.as_view(), name='venue-list-create'),
    path('<int:pk>/', VenueRetrieveUpdateDestroyView.as_view(), name='venue-retrieve-update-destroy'),
    path('paginated/', PaginatedVenueListView.as_view(), name='paginated-venue-list'),
]