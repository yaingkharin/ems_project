from django.urls import path
from app.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    PaginatedCategoryListView,
    CategoryRestoreView,
    CategoryPermanentDeleteView,
)

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='category-list-create'),
    path('<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('<int:pk>/restore/', CategoryRestoreView.as_view(), name='category-restore'),
    path('<int:pk>/permanent/', CategoryPermanentDeleteView.as_view(), name='category-permanent-delete'),
    path('paginate/', PaginatedCategoryListView.as_view(), name='category-paginate'),
]