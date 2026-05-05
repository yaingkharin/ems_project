from django.urls import path
from app.views.booking_views import (
    BookingListCreateView,
    BookingRetrieveUpdateDestroyView,
    PaginatedBookingListView,
    AdminBookingCreateView,
    BookingTicketDownloadView,
    BookingRestoreView,
    BookingPermanentDeleteView,
)

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('admin/', AdminBookingCreateView.as_view(), name='admin-booking-create'),
    path('<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
    path('<int:pk>/restore/', BookingRestoreView.as_view(), name='booking-restore'),
    path('<int:pk>/permanent/', BookingPermanentDeleteView.as_view(), name='booking-permanent-delete'),
    path('<int:pk>/ticket/', BookingTicketDownloadView.as_view(), name='booking-ticket-download'),
    path('paginate/', PaginatedBookingListView.as_view(), name='booking-paginate'),
]
