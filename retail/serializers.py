from rest_framework import serializers

from retail.models import Seller, Product, SellerProduct


class SellerProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи Продавца и Товара"""
    seller_title = serializers.CharField(
        source="seller.seller_title",
        read_only=True
    )
    product_title = serializers.CharField(
        source="product.product_title",
        read_only=True
    )
    supplier_title = serializers.CharField(
        source="supplier.seller_title",
        read_only=True
    )

    class Meta:
        model = SellerProduct
        fields = "__all__"
        read_only_fields = ["hierarchy_level", "debt", "created_at"]

    def validate(self, data):
        # Проверка, что поставщик не равен продавцу
        if data.get("seller") == data.get("supplier"):
            raise serializers.ValidationError({
                "supplier": "Продавец не может быть своим собственным поставщиком"
            })
        # Проверка, что связь уникальна
        seller = data.get("seller")
        product = data.get("product")
        supplier = data.get("supplier")

        if seller and product and supplier:
            existing = SellerProduct.objects.filter(
                seller=seller,
                product=product,
                supplier=supplier,
            ).exists()

            if existing and not self.instance:  # При создании нового объекта
                raise serializers.ValidationError({
                    "detail": "Такая связь уже существует"
                })

        return data


class SellerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Продавца"""

    total_debt = serializers.DecimalField(
        max_digits=11,
        decimal_places=2,
        read_only=True
    )
    effective_hierarchy_level = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Seller
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товара"""

    manufacturer_name = serializers.CharField(
        source="manufacturer.seller_title",
        read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"

    def validate_manufacturer(self, value):
        if value.seller_type not in [Seller.FACTORY, Seller.ENTREPRENEUR]:
            raise serializers.ValidationError(
                "Производителем может быть только завод или ИП"
            )
        return value
