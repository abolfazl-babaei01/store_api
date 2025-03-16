from .models import Cart
from .serializers import (CartSerializer, UpdateCartSerializer)
from rest_framework import viewsets, status, views
from rest_framework.response import Response


# Create your views here.


class CartViewSet(viewsets.ViewSet):
    """
    ViewSet for managing the user's cart.
    Retrieves and returns the list of items in the user's cart.
    """

    def list(self, request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCartView(views.APIView):
    """
    API view for adding, updating, or removing items from the user's cart.
    Ensures the cart exists and updates it based on the request data.
    """

    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = UpdateCartSerializer(instance=cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(cart, serializer.validated_data)
        return Response({'message': 'cart updated'}, status=status.HTTP_200_OK)
