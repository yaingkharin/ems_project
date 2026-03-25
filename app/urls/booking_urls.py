from django.urls import path
from app.views.booking_views import BookingListCreateView, BookingRetrieveUpdateDestroyView, PaginatedBookingListView, AdminBookingCreateView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('admin/', AdminBookingCreateView.as_view(), name='admin-booking-create'),
    path('<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
    path('paginate/', PaginatedBookingListView.as_view(), name='booking-paginate'),
]
