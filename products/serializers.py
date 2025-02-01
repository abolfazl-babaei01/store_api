from rest_framework import serializers
from products.models import Category, Product, ProductFuture, ProductGallery, ProductComment


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    This serializer provides all fields of the Category model.
    """

    class Meta:
        model = Category
        fields = '__all__'


class ProductFutureSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductFuture model.
    This serializer provides all fields of the ProductFuture model.
    """
    product = serializers.StringRelatedField()  # uses a StringRelatedField to display the product name

    class Meta:
        model = ProductFuture
        fields = '__all__'


class ProductGallerySerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductGallery model.
    This Serializer provides all fields of the ProductGallery model.
    """
    product = serializers.StringRelatedField()  # uses a StringRelatedField to display the product name

    class Meta:
        model = ProductGallery
        fields = '__all__'


class ProductCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductComment model.
    This Serializer for creating a product comment.
    """

    class Meta:
        model = ProductComment
        fields = ['product', 'name', 'body']


class ProductCommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductComment model.
    This Serializer provides `name` `body` `created` fields of the ProductComment model.
    """

    class Meta:
        model = ProductComment
        fields = ['name', 'body', 'created']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    This Serializer list products and display some fields of the Product model.

    """

    detail_url = serializers.HyperlinkedIdentityField(
        view_name='products:product_detail',
        lookup_field='slug') # This field is for displaying product details

    class Meta:
        model = Product
        fields = ['category', 'image',
                  'name', 'slug',
                  'description', 'price',
                  'new_price', 'detail_url']


class ProductDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for the Product model.
    This Serializer for product detail and display all fields of the Product model.
    """

    futures = ProductFutureSerializer(many=True, read_only=True)  # this filed for display product feature
    galleries = ProductGallerySerializer(many=True, read_only=True)  # this filed for display product galleries
    category = serializers.StringRelatedField()  # uses a StringRelatedField to display the category name
    comments = ProductCommentListSerializer(many=True, read_only=True)  # this filed for display product comments

    class Meta:
        model = Product

        fields = [
            'id', 'category', 'image',
            'name', 'slug',
            'description', 'inventory', 'price',
            'off', 'new_price','rating', 'created', 'updated', 'futures', 'galleries', 'comments']
