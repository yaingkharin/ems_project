from django.urls import path
from app.views.invoice_views import InvoiceListCreateView, InvoiceRetrieveUpdateDestroyView, PaginatedInvoiceListView

urlpatterns = [
    path('', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
    path('paginate/', PaginatedInvoiceListView.as_view(), name='invoice-paginate'),
]
