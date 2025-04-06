from rest_framework import generics, permissions
from .models import Ticket
from .serializers import (
    TicketCreateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    TicketMessageCreateSerializer
)


class UserTicketListView(generics.ListAPIView):
    """
    Returns a list of tickets created by the currently authenticated user.
    """
    serializer_class = TicketListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketDetailView(generics.RetrieveAPIView):
    """
    Retrieves the details and messages of a specific ticket owned by the current user.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(user=user)


class TicketCreateView(generics.CreateAPIView):
    """
    Allows the authenticated user to create a new support ticket.
    """
    serializer_class = TicketCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class TicketMessageCreateView(generics.CreateAPIView):
    """
    Allows the user to add a message to an existing ticket.
    """
    serializer_class = TicketMessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
