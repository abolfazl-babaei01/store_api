from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('', views.UserTicketListView.as_view(), name='ticket-list'),
    path('create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:ticket_id>/messages/create/', views.TicketMessageCreateView.as_view(), name='ticket-message-create'),
]
