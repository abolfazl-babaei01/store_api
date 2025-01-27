from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'cart'

router = SimpleRouter()
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('remove-item/', views.RemoveCartItemView.as_view(), name='remove_item'),
    path('delete-item/', views.DeleteCartItemView.as_view(), name='delete_item'),
]
urlpatterns += router.urls

