import django_filters

from reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    min_rate=django_filters.NumberFilter(field_name='rate', lookup_expr='gte')
    max_rate=django_filters.NumberFilter(field_name='rate', lookup_expr='lte')

    class Meta:
        model = Review
        fields = {}