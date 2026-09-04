import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    brand = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='gte')
    max_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='lte')
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
       }