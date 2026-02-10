from django.urls import path
from app.views.ticket_views import TicketListCreateView, TicketRetrieveUpdateDestroyView, PaginatedTicketListView

urlpatterns = [
    path('', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('<int:pk>/', TicketRetrieveUpdateDestroyView.as_view(), name='ticket-retrieve-update-destroy'),
    path('paginate/', PaginatedTicketListView.as_view(), name='ticket-paginate'),
]