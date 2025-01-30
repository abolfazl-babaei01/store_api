from rest_framework.response import Response
from rest_framework import views, status, generics, permissions
from .serializers import OrderSerializer, CreateOrderSerializer
from django.db import transaction

from .models import Order, OrderItem
from cart.models import Cart

# Create your views here.


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).all()



class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
