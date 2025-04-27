from django.urls import path
from . import views


app_name = 'info'

urlpatterns = [
    path('about-us/', views.AboutUsApiView.as_view(), name='about-us'),
    path('privacy/', views.PrivacyApiView.as_view(), name='privacy'),
    path('faq/', views.FAQApiView.as_view(), name='faqs'),
    path('terms/', views.TermsAndConditionsApiView.as_view(), name='terms'),
    path('contact/', views.ContactInfoApiView.as_view(), name='contact'),
]