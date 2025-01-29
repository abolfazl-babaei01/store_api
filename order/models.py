from django.db import models
from accounts.models import CustomUser, Address
from products.models import Product
from utils.validators import phone_regex

# Create your models here.


class Order(models.Model):

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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone} - {self.first_name} {self.last_name}'

    class Meta:
        ordering = ['-created']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'



class OrderItem(models.Model):
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

