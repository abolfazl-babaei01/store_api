from itertools import product

from rest_framework import serializers

from products.models import Product
from .models import Cart, CartItem



class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created', 'cart_total_price', 'items']

class AddToCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        if product.inventory < data['quantity']:
            raise serializers.ValidationError('Inventory is less than quantity')
        return data

    def create(self, validated_data):
        user = self.context['request'].user

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=validated_data['product_id'])

        cart_item.quantity += validated_data['quantity']
        cart_item.save()
        return cart_item