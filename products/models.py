from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Category(models.Model):
    """
    Category model for products model
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='name'),
        ]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

class Product(models.Model):
    """
    Product model.
    This model is for creating products.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') # product category . . .
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    image = models.ImageField(upload_to='products/images/')  # first image , show in products list
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    inventory = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)  # amount of discount
    new_price = models.PositiveIntegerField(default=0)  # price after discount (calculated automatic)

    rating = models.PositiveIntegerField(null=True, blank=True,
                                         validators=[MinValueValidator(1), MaxValueValidator(5)]
                                         )

    color_code = models.CharField(max_length=7, default='#FFFFFF')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug'], name='slug'),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def save(self, *args, **kwargs):
        """
        overriding save method for product model.
        Price calculation after discount and save to new price field.
        """
        if self.off == 0:
            self.new_price = self.price
        self.new_price = self.price - self.off
        super().save(*args, **kwargs)


class ProductGallery(models.Model):
    """
    ProductGallery model.
    This model is for add image in to product galleries.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='galleries') # select target product
    file = models.ImageField(upload_to='products/galleries/') # add image file

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'ProductGallery'
        verbose_name_plural = 'ProductGalleries'



class ProductFuture(models.Model):
    """
    ProductFuture model.
    This model is for add feature in to product features.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='futures') # select target product
    name = models.CharField(max_length=200) # future name : future value
    value = models.CharField(max_length=200) # ^^^^^^^^^^^^^^^^^^^^^^^^^

    def __str__(self):
        return self.name

class ProductComment(models.Model):
    """
    ProductComment model.
    This model is for add comment to products.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    star = models.PositiveIntegerField(null=True, blank=True,
                                         validators=[MinValueValidator(1), MaxValueValidator(5)], default=4)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = 'Product Comment'
        verbose_name_plural = 'Product Comments'