from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('addresses', views.AddressViewSet, basename='address')

app_name = 'accounts'

urlpatterns = [
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),

    # Auth (OTP)
    path('auth/otp/request/', views.OTPRequestView.as_view(), name='auth-otp-request'),
    path('auth/otp/verify/', views.OTPVerifyView.as_view(), name='auth-otp-verify'),

    # User Profile
    path('profile/', views.UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),

    # Password Management
    path('profile/reset-password/', views.ResetPasswordView.as_view(), name='profile-reset-password'),

    # Phone Number
    path('profile/change-phone/', views.ChangePhoneNumberView.as_view(), name='profile-change-phone'),

    # User Activity
    path('profile/latest-comments/', views.UserCommentsView.as_view(), name='profile-latest-comments'),
    path('favorites/toggle/', views.FavoriteProductToggleAPIView.as_view(), name='favorite-toggle'),
    path('profile/favorites/', views.FavoriteProductListAPIView.as_view(), name='favorite-list'),

]

urlpatterns += router.urls
