from rest_framework import serializers
from products.models import Product
from .models import Cart, CartItem
from .services import update_cart


class CartItemSerializer(serializers.ModelSerializer):
    """
    This Serializer for CartItem model and provide all CartItem fields.
    """
    product = serializers.StringRelatedField() # display product name

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total_price']


class CartSerializer(serializers.ModelSerializer):
    """
    This Serializer for Cart model and provide all Cart fields.
    """
    items = CartItemSerializer(many=True) # for serializing cart items
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created', 'cart_total_price', 'items']


# class BaseCartActionsSerializer(serializers.Serializer):
#     """
#     BaseCartActionsSerializer:
#     Serializes and validates cart actions by ensuring the product and quantity are valid.
#     """
#     product_id = serializers.IntegerField()
#     quantity = serializers.IntegerField(min_value=1)
#
#     def validate(self, data):
#         try:
#             product = Product.objects.get(pk=data['product_id'])
#         except Product.DoesNotExist:
#             raise serializers.ValidationError('hey! Product does not exist')
#         data['product'] = product #Add the validated Product instance to the data
#         return data
#
#
# class AddItemToCartSerializer(BaseCartActionsSerializer):
#     """
#     AddItemToCartSerializer:
#     Handles adding items to the user's cart while ensuring inventory availability.
#     """
#
#     def create(self, validated_data):
#         user = self.context['request'].user
#
#         cart, created = Cart.objects.get_or_create(user=user)
#         product = Product.objects.get(pk=validated_data['product_id'])
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         # check product inventory
#         if cart_item.quantity < product.inventory:
#             cart_item.quantity += validated_data['quantity']
#         else:
#             raise serializers.ValidationError('The number of inputs is not available in stock')
#         cart_item.save()
#         return cart_item
#
#
# class DecreaseItemFromCartSerializer(BaseCartActionsSerializer):
#     """
#     DecreaseItemFromCartSerializer:
#     Handles decreasing the quantity of an item in the user's cart, ensuring the remaining quantity is valid.
#     """
#
#     def update(self, instance, validated_data):
#
#         cart_item = CartItem.objects.filter(cart=instance, product=validated_data['product']).first()
#         if not cart_item:
#             raise serializers.ValidationError('Cart item not found.')
#
#         # check item quantity
#         if cart_item.quantity == 1:
#             raise serializers.ValidationError('Quantity to remove is greater than or equal to current quantity.')
#
#         cart_item.quantity -= validated_data['quantity']
#         cart_item.save()
#         return cart_item
#
#
# class DeleteItemFromCartSerializer(serializers.Serializer):
#     """
#     DeleteItemFromCartSerializer:
#     Handles the removal of an item from the user's cart based on the provided product ID.
#     """
#     product_id = serializers.IntegerField(required=True)
#
#     def validate(self, data):
#         try:
#             product = Product.objects.get(pk=data['product_id'])
#         except Product.DoesNotExist:
#             raise serializers.ValidationError('hey! Product does not exist')
#         data['product'] = product
#         return data
#
#     def update(self, instance, validated_data):
#         cart_item = CartItem.objects.filter(cart=instance, product=validated_data['product']).first()
#         if not cart_item:
#             raise serializers.ValidationError('Cart item not found.')
#         cart_item.delete()
#         return cart_item


class UpdateCartSerializer(serializers.Serializer):

    """
    This Serializer for Update cart.
    Supported add item in cart and remove item in cart.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    action = serializers.ChoiceField(choices=['add', 'remove'])


    def validate(self, data):
        product_id = data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        return data


    def update(self, instance, validated_data):
        cart = instance
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        action = validated_data['action']

        update_cart(cart, product_id, quantity, action)
        return cart