from django.urls import path
from app.views.venue_views import (
    VenueListCreateView,
    VenueRetrieveUpdateDestroyView,
    PaginatedVenueListView,
    VenueRestoreView,
    VenuePermanentDeleteView,
)

urlpatterns = [
    path('', VenueListCreateView.as_view(), name='venue-list-create'),
    path('<int:pk>/', VenueRetrieveUpdateDestroyView.as_view(), name='venue-retrieve-update-destroy'),
    path('<int:pk>/restore/', VenueRestoreView.as_view(), name='venue-restore'),
    path('<int:pk>/permanent/', VenuePermanentDeleteView.as_view(), name='venue-permanent-delete'),
    path('paginated/', PaginatedVenueListView.as_view(), name='paginated-venue-list'),
]