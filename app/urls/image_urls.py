from django.urls import path
from app.views.image_views import ImageListCreateView, ImageRetrieveUpdateDestroyView, PaginatedImageListView

urlpatterns = [
    path('', ImageListCreateView.as_view(), name='images-list-create'),
    path('paginate/', PaginatedImageListView.as_view(), name='images-paginate'),
    path('<int:pk>/', ImageRetrieveUpdateDestroyView.as_view(), name='images-detail'),
]
