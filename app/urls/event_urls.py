from django.urls import path
from app.views.event_views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    PaginatedEventListView,
    EventRestoreView,
    EventPermanentDeleteView,
)

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('<int:pk>/restore/', EventRestoreView.as_view(), name='event-restore'),
    path('<int:pk>/permanent/', EventPermanentDeleteView.as_view(), name='event-permanent-delete'),
    path('paginate/', PaginatedEventListView.as_view(), name='event-paginate'),
]