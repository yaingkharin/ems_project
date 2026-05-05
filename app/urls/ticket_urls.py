from django.urls import path
from app.views.ticket_views import (
    TicketListCreateView,
    TicketRetrieveUpdateDestroyView,
    PaginatedTicketListView,
    TicketRestoreView,
    TicketPermanentDeleteView,
)

urlpatterns = [
    path('', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('<int:pk>/', TicketRetrieveUpdateDestroyView.as_view(), name='ticket-retrieve-update-destroy'),
    path('<int:pk>/restore/', TicketRestoreView.as_view(), name='ticket-restore'),
    path('<int:pk>/permanent/', TicketPermanentDeleteView.as_view(), name='ticket-permanent-delete'),
    path('paginate/', PaginatedTicketListView.as_view(), name='ticket-paginate'),
]