from django.db import models
from accounts.models import CustomUser
from products.models import Product


# Create your models here.


class Cart(models.Model):
    """
    Cart Model
    This Model is used to store the cart
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def cart_total_price(self):
        """
        The sum total of the shopping cart prices
        """
        return sum(item.item_total_price for item in self.items.all())


class CartItem(models.Model):
    """
    CartItem Model
    This Model is used to store the cart item
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=0)

    @property
    def item_total_price(self):
        """
        The sum total price of the items cart
        """
        return self.quantity * self.product.new_price
