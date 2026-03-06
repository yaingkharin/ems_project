from django.urls import path
from app.views.event_registration_views import EventRegistrationListCreateView, EventRegistrationRetrieveUpdateDestroyView, PaginatedEventRegistrationListView

urlpatterns = [
    path('', EventRegistrationListCreateView.as_view(), name='event-registration-list-create'),
    path('<int:pk>/', EventRegistrationRetrieveUpdateDestroyView.as_view(), name='event-registration-retrieve-update-destroy'),
    path('paginate/', PaginatedEventRegistrationListView.as_view(), name='event-registration-paginate'),
]
