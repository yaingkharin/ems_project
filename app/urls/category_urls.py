from django.urls import path
from app.views.category_views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView, PaginatedCategoryListView

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='category-list-create'),
    path('<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('paginate/', PaginatedCategoryListView.as_view(), name='category-paginate'),
]