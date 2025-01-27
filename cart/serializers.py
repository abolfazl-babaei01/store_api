from rest_framework import serializers
from select import select

from products.models import Product
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created', 'cart_total_price', 'items']


class BaseCartActionsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('hey! Product does not exist')
        data['product'] = product
        return data


class AddItemToCartSerializer(BaseCartActionsSerializer):
    def create(self, validated_data):
        user = self.context['request'].user

        cart, created = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk=validated_data['product_id'])
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # check product inventory
        if cart_item.quantity < product.inventory:
            cart_item.quantity += validated_data['quantity']
        else:
            raise serializers.ValidationError('The number of inputs is not available in stock')
        cart_item.save()
        return cart_item


class RemoveItemFromCartSerializer(BaseCartActionsSerializer):

    def update(self, instance, validated_data):

        cart_item = CartItem.objects.filter(cart=instance, product=validated_data['product']).first()
        if not cart_item:
            raise serializers.ValidationError('Cart item not found.')

        # check item quantity
        if cart_item.quantity == 1:
            raise serializers.ValidationError('Quantity to remove is greater than or equal to current quantity.')

        cart_item.quantity -= validated_data['quantity']
        cart_item.save()
        return cart_item


class DeleteItemFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('hey! Product does not exist')
        data['product'] = product
        return data

    def update(self, instance, validated_data):
        cart_item = CartItem.objects.filter(cart=instance, product=validated_data['product']).first()
        if not cart_item:
            raise serializers.ValidationError('Cart item not found.')
        cart_item.delete()
        return cart_item
