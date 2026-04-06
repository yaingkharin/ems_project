from django.urls import path
from app.views.event_ticket_views import EventTicketListCreateView, EventTicketRetrieveUpdateDestroyView, PaginatedEventTicketListView

urlpatterns = [
    path('', EventTicketListCreateView.as_view(), name='event-ticket-list-create'),
    path('<int:pk>/', EventTicketRetrieveUpdateDestroyView.as_view(), name='event-ticket-retrieve-update-destroy'),
    path('paginate/', PaginatedEventTicketListView.as_view(), name='event-ticket-paginate'),
]
