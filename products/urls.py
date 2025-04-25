from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),

    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('features/', views.ProductFutureListView.as_view(), name='features'),
    path('galleries/', views.ProductGalleryListView.as_view(), name='galleries'),

    path('create-comment/', views.ProductCommentCreateView.as_view(), name='product_add_comment'),

    path('<slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]