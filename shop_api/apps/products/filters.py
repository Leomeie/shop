import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    min_price = django_filters.NumberFilter(method="filter_min_price")
    max_price = django_filters.NumberFilter(method="filter_max_price")
    is_featured = django_filters.BooleanFilter()
    status = django_filters.CharFilter()

    class Meta:
        model = Product
        fields = ["category", "is_featured", "status"]

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(skus__price__gte=value, skus__is_active=True).distinct()

    def filter_max_price(self, queryset, name, value):
        return queryset.filter(skus__price__lte=value, skus__is_active=True).distinct()
