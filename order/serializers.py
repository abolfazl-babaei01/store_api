from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer
from accounts.serializers import AddressSerializer
from utils.validators import phone_regex
from accounts.models import Address
from cart.models import Cart

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializes order items, including product details, quantity, and price.
    """
    product = ProductListSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    """
    Serializes order details, including buyer info, address, items, and total price.
    """
    items = OrderItemSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'first_name', 'last_name', 'phone', 'status', 'address', 'items'
            , 'total_price', 'created']


class CreateOrderSerializer(serializers.Serializer):

    """
    Serializer for creating an order.
    - Validates the provided address to ensure it belongs to the requesting user.
    - Checks if the user's cart exists and contains items.
    - Creates an order and its related order items.
    - Calculates and assigns the total order price.
    """


    first_name = serializers.CharField(max_length=200, required=True)
    last_name = serializers.CharField(max_length=200, required=True)
    phone = serializers.CharField(max_length=11, required=True, validators=[phone_regex])
    address_id = serializers.IntegerField()

    def validate(self, data):
        user = self.context["request"].user
        try:
            address = Address.objects.get(pk=data['address_id'], user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError('Address does not exist')
        data['address'] = address # the add validated address in data
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        if not cart or not cart.items.exists():
            raise serializers.ValidationError('cart not found or cart is empty')

        order = Order.objects.create(buyer=user, address=validated_data['address'],
                                     first_name=validated_data['first_name'],last_name=validated_data['last_name'],
                                     phone=validated_data['phone'],)
        total_price = 0

        for item in cart.items.all():
            OrderItem.objects.create(order=order,
                                     product=item.product,
                                     quantity=item.quantity,
                                     price=item.product.new_price)
            total_price += item.product.new_price * item.quantity

        order.total_price = total_price
        order.save()

        # cart.items.all().delete()
        return order
