from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
]
