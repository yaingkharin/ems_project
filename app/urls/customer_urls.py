from django.urls import path
from app.views.customer_views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView, PaginatedCustomerListView

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('paginate/', PaginatedCustomerListView.as_view(), name='customers-paginate'),
    path('<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customers-detail'),
]
