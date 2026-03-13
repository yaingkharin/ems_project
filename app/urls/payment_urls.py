from django.urls import path
from app.views.payment_views import (
    PaymentListCreateView, 
    PaymentRetrieveUpdateDestroyView, 
    PaginatedPaymentListView,
    GenerateBakongQRView,
    CheckBakongStatusView,
    TestBakongPaymentView,
    TestBakongCheckStatusView
)

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-retrieve-update-destroy'),
    path('paginate/', PaginatedPaymentListView.as_view(), name='payment-paginate'),
    path('<int:pk>/bakong-qr/', GenerateBakongQRView.as_view(), name='payment-bakong-qr'),
    path('check-status/', CheckBakongStatusView.as_view(), name='payment-check-status'),
    path('test-bakong/', TestBakongPaymentView.as_view(), name='test-bakong'),
    path('test-bakong-status/', TestBakongCheckStatusView.as_view(), name='test-bakong-status'),
]