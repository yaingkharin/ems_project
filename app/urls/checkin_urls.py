from django.urls import path
from app.views.checkin_views import (
    CheckinListCreateView, 
    CheckinRetrieveUpdateDestroyView, 
    PaginatedCheckinListView,
    ValidateTicketView,
    ConfirmCheckinView
)

urlpatterns = [
    path('', CheckinListCreateView.as_view(), name='checkin-list-create'),
    path('<int:pk>/', CheckinRetrieveUpdateDestroyView.as_view(), name='checkin-retrieve-update-destroy'),
    path('paginate/', PaginatedCheckinListView.as_view(), name='checkin-paginate'),
    path('validate/', ValidateTicketView.as_view(), name='checkin-validate'),
    path('confirm/', ConfirmCheckinView.as_view(), name='checkin-confirm'),
]