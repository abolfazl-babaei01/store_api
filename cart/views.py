from django.shortcuts import render

from .models import Cart
from .serializers import CartItemSerializer, CartSerializer, AddToCartItemSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
# Create your views here.


class CartViewSet(viewsets.ViewSet):

    def list(self, request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = AddToCartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




