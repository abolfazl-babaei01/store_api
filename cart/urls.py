from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'cart'

router = SimpleRouter()
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = router.urls

