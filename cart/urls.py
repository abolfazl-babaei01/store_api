from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'cart'

router = SimpleRouter()
router.register('items', views.CartViewSet, basename='cart-items')

urlpatterns = [
    path('update/', views.UpdateCartView.as_view(), name='cart-update'),
]

urlpatterns += router.urls
