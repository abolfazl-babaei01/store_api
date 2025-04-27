from rest_framework.response import Response
from rest_framework import views, status, generics, permissions
from .serializers import OrderListSerializer, OrderDetailSerializer, CreateOrderSerializer
from django.db import transaction

from .models import Order, OrderItem
from cart.models import Cart


# Create your views here.


class OrderListView(generics.ListAPIView):
    """
    Lists all orders placed by the authenticated user.
    Only orders belonging to the current user are returned."""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).all()


class OrderDetailView(generics.RetrieveAPIView):
    """
    Retrieves detailed information about a specific order.
    Ensures that the order belongs to the authenticated user.
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).all()


class CreateOrderView(views.APIView):
    """
    Handles the creation of a new order by the authenticated user.
    Validates and saves order data within a transaction.
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
