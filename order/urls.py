from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('create/', views.CreateOrderView.as_view(), name='order-create'),
]
