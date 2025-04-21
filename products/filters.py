import django_filters
from .models import Product
from django.utils import timezone
from datetime import timedelta


class ProductFilter(django_filters.FilterSet):
    """
    Custom filters for the Product model.
    Allows filtering by price range, category slug, availability, and recent products.
    """

    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    category = django_filters.CharFilter(field_name='category__slug')

    available = django_filters.BooleanFilter(method='filter_available')
    new = django_filters.BooleanFilter(method='filter_new')

    def filter_available(self, queryset, name, value):
        """Filter products that are in stock."""
        if value:
            return queryset.filter(inventory__gt=0)
        return queryset

    def filter_new(self, queryset, name, value):
        """Filter products created within the last 7 days."""
        if value:
            last_week = timezone.now() - timedelta(days=7)
            return queryset.filter(created__gte=last_week)
        return queryset

    class Meta:
        model = Product
        fields = []
