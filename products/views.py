from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product, Category, ProductFuture, ProductGallery, ProductComment
from .serializers import (ProductListSerializer, ProductDetailSerializer, CategorySerializer, ProductFutureSerializer,
                          ProductGallerySerializer,
                          ProductCommentCreateSerializer)

from .paginations import BasePagination


# Create your views here.


class ProductListView(generics.ListAPIView):
    """
    This View provides a list of all products.
    Supported methods: [GET]
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = BasePagination


class ProductDetailView(generics.RetrieveAPIView):
    """
    This View provides a detail view of a single product
    and display `comments` `categories` `features` `galleries` related fields.
    Supported methods: [GET]
    """
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CategoryListView(generics.ListAPIView):
    """
    This View provides a list of all categories.
    Supported methods: [GET]
    """
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasePagination


class ProductFutureListView(generics.ListAPIView):
    """
    This View provides a list of all product futures.
    Supported methods: [GET]
    """
    permission_classes = [AllowAny]
    queryset = ProductFuture.objects.all()
    serializer_class = ProductFutureSerializer


class ProductGalleryListView(generics.ListAPIView):
    """
    This View provides a list of all product galleries.
    Supported methods: [GET]
    """
    permission_classes = [AllowAny]
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer


class ProductCommentCreateView(generics.CreateAPIView):
    """
    This view provides create new comment for products.
    Supported methods: [POST]
    """
    throttle_scope = 'comment'  # two request in one hour

    permission_classes = [AllowAny]
    serializer_class = ProductCommentCreateSerializer
    queryset = ProductComment.objects.all()
