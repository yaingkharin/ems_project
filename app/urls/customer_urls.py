from django.urls import path
from app.views.customer_views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroyView,
    PaginatedCustomerListView,
    CustomerMeView,
    CustomerRestoreView,
    CustomerPermanentDeleteView,
)

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('me/', CustomerMeView.as_view(), name='customers-me'),
    path('paginate/', PaginatedCustomerListView.as_view(), name='customers-paginate'),
    path('<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customers-detail'),
    path('<int:pk>/restore/', CustomerRestoreView.as_view(), name='customers-restore'),
    path('<int:pk>/permanent/', CustomerPermanentDeleteView.as_view(), name='customers-permanent-delete'),
]
