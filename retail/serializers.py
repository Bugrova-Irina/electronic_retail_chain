from rest_framework import serializers

from retail.models import Product, Seller, SellerProduct


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
        read_only_fields = ["hierarchy_level"]

    def validate(self, data):
        # Для PATCH-запросов используем существующие значения из instance
        seller = data.get("seller", getattr(self.instance, "seller", None) if self.instance else data.get("seller"))
        supplier = data.get(
            "supplier", getattr(self.instance, "supplier", None) if self.instance else data.get("supplier")
        )

        # Проверка, что поставщик не равен продавцу
        if seller and supplier and seller == supplier:
            raise serializers.ValidationError({
                "supplier": "Продавец не может быть своим собственным поставщиком"
            })
        # Проверка, что связь уникальна (только для создания)
        if not self.instance:  # Только при создании нового объекта
            seller = data.get("seller")
            product = data.get("product")
            supplier = data.get("supplier")

            if seller and product and supplier:
                existing = SellerProduct.objects.filter(
                    seller=seller,
                    product=product,
                    supplier=supplier,
                ).exists()

                if existing:
                    raise serializers.ValidationError({
                        "detail": "Такая связь уже существует"
                    })

        return data

    # Явно запрещаем обновление поля debt при PUT/PATCH запросах
    def update(self, instance, validated_data):
        # Удаляем debt из validate_data, если он там есть
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)


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
