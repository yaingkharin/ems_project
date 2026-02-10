from django.urls import path
from app.views.test_views import TestListCreateView,TestRetrieveUpdateDestroyView,PaginatedTestListView

urlpatterns = [
    path('', TestListCreateView.as_view(), name='test-list-create'),
    path('<int:pk>/', TestRetrieveUpdateDestroyView.as_view(), name='test-retrieve-update-destroy'),
    path('paginated/', PaginatedTestListView.as_view(), name='paginated-test-list'),
]