from django.db import models


class Seller(models.Model):
    """Модель продавца - только общая информация"""

    # Вид продавца
    FACTORY = "factory"
    RETAIL = "retail"
    ENTREPRENEUR = "entrepreneur"

    TYPE_SELLER_CHOICE = [
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "Индивидуальный предприниматель"),
    ]

    seller_title = models.CharField(
        max_length=300,
        verbose_name="Название",
        help_text="Укажите название",
    )
    seller_type = models.CharField(
        max_length=12,
        choices=TYPE_SELLER_CHOICE,
        default=RETAIL,
        verbose_name="Тип продавца",
        help_text="Выберите тип продавца",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту",
    )
    country = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Укажите страну",
    )
    city = models.CharField(
        max_length=150,
        verbose_name="Город",
        help_text="Укажите город",
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=200,
        verbose_name="Улица",
        help_text="Укажите улицу",
        blank=True,
        null=True,
    )
    house_number = models.CharField(
        max_length=15,
        verbose_name="Номер дома",
        help_text="Укажите номер дома",
        blank=True,
        null=True,
    )
    creation_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        help_text="Укажите время создания",
    )

    @property
    def total_debt(self):
        """Общая задолженность перед всеми поставщиками"""
        return (
            self.sellerproduct_set.aggregate(total_debt=models.Sum("debt"))[
                "total_debt"
            ]
            or 0
        )

    @property
    def min_hierarchy_level(self):
        """Минимальный уровень иерархии среди всех товаров продавца"""
        min_level = SellerProduct.objects.filter(seller=self).aggregate(
            min_level=models.Min("hierarchy_level")
        )["min_level"]
        return min_level if min_level is not None else 0

    @property
    def max_hierarchy_level(self):
        """Максимальный уровень иерархии среди всех товаров продавца"""
        max_level = SellerProduct.objects.filter(seller=self).agregate(
            max_level=models.Max("hierarchy_level")
        )["max_level"]
        return max_level if max_level is not None else 0

    def get_hierarchy_for_product(self, product):
        """Уровень иерархии для конкретного товара"""
        try:
            # Находим поставщика для этого товара через SellerProduct
            seller_product = SellerProduct.objects.get(seller=self, product=product)
            return seller_product.hierarchy_level
        except SellerProduct.DoesNotExist:
            return 0

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    def __str__(self):
        return f"{self.seller_title} - {self.seller_type}"


class Product(models.Model):
    """Модель товара - только общая информация"""

    product_title = models.CharField(
        max_length=300,
        verbose_name="Название товара",
        help_text="Укажите название товара",
    )
    product_model = models.CharField(
        max_length=150,
        verbose_name="Модель товара",
        help_text="Укажите модель товара",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание товара",
        help_text="Укажите описание товара",
    )
    manufacturer = models.ForeignKey(
        "retail.Seller",
        on_delete=models.PROTECT,
        limit_choices_to={"seller_type__in": [Seller.FACTORY, Seller.ENTREPRENEUR]},
        verbose_name="Производитель",
        help_text="Укажите производителя (завод или ИП)",
    )
    product_launch_date = models.DateField(
        verbose_name="Дата выхода товара на рынок",
        help_text="Укажите дату выхода товара на рынок",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.product_title} {self.product_model}"


class SellerProduct(models.Model):
    """Связь продавца с товаром (складские остатки, цены)"""

    seller = models.ForeignKey(
        "retail.Seller",
        on_delete=models.CASCADE,
        verbose_name="Продавец",
        help_text="Укажите продавца",
    )
    product = models.ForeignKey(
        "retail.Product",
        on_delete=models.CASCADE,
        verbose_name="Товар",
        help_text="Укажите товар",
    )
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена товара",
        help_text="Укажите цену товара",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество товара",
        help_text="Укажите количество товара",
    )
    supplier = models.ForeignKey(
        "retail.Seller",
        on_delete=models.PROTECT,
        related_name="supplied_items",
        verbose_name="Поставщик этого товара",
        help_text="Укажите поставщика этого товара",
    )
    debt = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность за этот товар",
        help_text="Укажите задолженность за этот товар с копейками в формате 0.00",
    )
    hierarchy_level = models.IntegerField(
        default=0,
        verbose_name="Уровень иерархии для этой связи",
        help_text="Укажите уровень иерархии для этой связи",
    )

    class Meta:
        verbose_name = "Связь продавца с товаром"
        verbose_name_plural = "Связи продавцов с товарами"
        unique_together = ["seller", "product", "supplier"]

    def save(self, *args, **kwargs):
        # Вычисляем уровень иерархии при сохранении
        if self.supplier:
            if self.supplier.seller_type == Seller.FACTORY:
                self.hierarchy_level = 1
            else:
                # Находим уровень поставщика для этого же товара и добавляем 1
                supplier_product = SellerProduct.objects.filter(
                    seller=self.supplier, product=self.product
                ).first()

                if supplier_product:
                    self.hierarchy_level = supplier_product.hierarchy_level + 1
                else:
                    # Если у поставщика нет этого товара, считаем уровень 1
                    self.hierarchy_level = 1
        else:
            self.hierarchy_level = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.seller} - {self.product} (Уровень: {self.hierarchy_level})"
