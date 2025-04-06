from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/message/create/', views.TicketMessageCreateView.as_view(), name='ticket_message_create'),
    path('tickets/', views.UserTicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
]
