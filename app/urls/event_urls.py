from django.urls import path
from app.views.event_views import EventListCreateView, EventRetrieveUpdateDestroyView, PaginatedEventListView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('paginate/', PaginatedEventListView.as_view(), name='event-paginate'),
]