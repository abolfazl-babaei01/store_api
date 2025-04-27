from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('features/', views.ProductFutureListView.as_view(), name='feature-list'),
    path('galleries/', views.ProductGalleryListView.as_view(), name='gallery-list'),
    path('comments/create/', views.ProductCommentCreateView.as_view(), name='product-comment-create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
