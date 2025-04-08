from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('mark-all-as-read/', views.MarkAllNotificationsReadView.as_view(), name='mark_all_as_read'),
]
