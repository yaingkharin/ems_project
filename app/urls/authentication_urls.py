from django.urls import path
from app.views.authentication_views import AuthenticationListCreateView, AuthenticationRetrieveUpdateDestroyView, PaginatedAuthenticationListView

urlpatterns = [
    path('', AuthenticationListCreateView.as_view(), name='authentications-list-create'),
    path('paginate/', PaginatedAuthenticationListView.as_view(), name='authentications-paginate'),
    path('<int:pk>/', AuthenticationRetrieveUpdateDestroyView.as_view(), name='authentications-detail'),
]
