from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('addresses', views.AddressViewSet, basename='address')


app_name = 'accounts'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('otp-request/', views.OTPRequestView.as_view(), name='otp_request'),
    path('otp-verify/', views.OTPVerifyView.as_view(), name='otp_verify'),

    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('change-phone/', views.ChangePhoneNumberView.as_view(), name='change_phone'),

]

urlpatterns += router.urls

