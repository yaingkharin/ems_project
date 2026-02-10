from django.urls import path
from app.views.booking_views import BookingListCreateView, BookingRetrieveUpdateDestroyView, PaginatedBookingListView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
    path('paginate/', PaginatedBookingListView.as_view(), name='booking-paginate'),
]
