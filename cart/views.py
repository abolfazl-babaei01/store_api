from .models import Cart
from .serializers import (CartSerializer, AddItemToCartSerializer, RemoveItemFromCartSerializer,
                          DeleteItemFromCartSerializer)
from rest_framework import viewsets, status, views
from rest_framework.response import Response
# Create your views here.


class CartViewSet(viewsets.ViewSet):

    def list(self, request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = AddItemToCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RemoveCartItemView(views.APIView):
    def put(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RemoveItemFromCartSerializer(instance=cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCartItemView(views.APIView):
    def put(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DeleteItemFromCartSerializer(instance=cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product Item deleted in Cart'}, status=status.HTTP_200_OK)