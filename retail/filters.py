import django_filters
from .models import Seller


class SupplierFilter(django_filters.FilterSet):
    has_products = django_filters.BooleanFilter(
        method="filter_has_product",
        label="Имеет поставляемые товары"
    )
    supplier_type = django_filters.ChoiceFilter(
        field_name="seller_type",
        choices=Seller.TYPE_SELLER_CHOICE,
        label="Тип поставщика"
    )

    class Meta:
        model = Seller
        fields = ["country", "city", "seller_type"]

    def filter_has_products(self, queryset, name, value):
        if value:
            return queryset.filter(supplied_items__isnull=False).distinct()
        return queryset
