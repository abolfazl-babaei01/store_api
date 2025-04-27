from django.db import models
from accounts.models import CustomUser, Address
from products.models import Product
from utils.validators import phone_regex

import uuid
from django.core.exceptions import ValidationError


# Create your models here.

def generate_order_code():
    """
    Generates a unique 10-character order code.
    The code is created by generating a UUID, converting it to an integer, and extracting the first 9 digits.
    """

    unique_number = int(uuid.uuid4().int >> 64)
    unique_digits = str(unique_number)[:9]

    order_code = '2' + unique_digits
    return order_code


class Order(models.Model):
    """
    Represents an order placed by a user.
    Includes buyer information, order status, total price, and unique order code.
    """

    class OrderStatus(models.TextChoices):
        pending = ('pending', 'PENDING')
        shipped = ('shipped', 'SHIPPED')
        delivered = ('delivered', 'DELIVERED')
        canceled = ('canceled', 'CANCELLED')

    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11, validators=[phone_regex])
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address')
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.pending)
    total_price = models.PositiveBigIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    order_code = models.CharField(max_length=10, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone} - {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """
        Generates a unique order code if not already present.
        Tries 5 times to create a unique code. Raises an error if a unique code cannot be generated.
        """
        if not self.order_code:
            for _ in range(5):
                code = generate_order_code()
                if not Order.objects.filter(order_code=code).exists():
                    self.order_code = code
                    break
            else:
                raise ValidationError("Could not generate a unique order code. Please try again.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    """
    Represents an item within an order, including the product, quantity, and price.
    Links each item to a specific order and product.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveBigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} {self.price}'

    class Meta:
        ordering = ['-created']
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
