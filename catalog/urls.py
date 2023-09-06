from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from . import views
from .views import contacts, IndexView, ProductDetailView, blog_list_view, ProductCreateView, ProductDeleteView, \
    ProductUpdateView, CategoryListView


app_name = CatalogConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('list/', blog_list_view, name='catalog_list'),
    path('categories/', cache_page(60 * 15)(CategoryListView.as_view()), name='categories'),
    path('category/<int:pk>/', cache_page(60 * 15)(views.CategoryDetailView.as_view()), name='category_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
