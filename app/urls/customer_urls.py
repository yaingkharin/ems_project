from django.urls import path
from app.views.customer_views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView, PaginatedCustomerListView, CustomerMeView

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('me/', CustomerMeView.as_view(), name='customers-me'),
    path('paginate/', PaginatedCustomerListView.as_view(), name='customers-paginate'),
    path('<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customers-detail'),
]
