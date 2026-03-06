from django.urls import path
from app.views.payment_views import PaymentListCreateView, PaymentRetrieveUpdateDestroyView, PaginatedPaymentListView

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-retrieve-update-destroy'),
    path('paginate/', PaginatedPaymentListView.as_view(), name='payment-paginate'),
]