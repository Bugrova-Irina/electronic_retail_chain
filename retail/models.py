from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    """Модель товара"""

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
    price = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Укажите цену"
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


class Seller(models.Model):
    """Модель продавца"""

    # Вид продавца
    FACTORY = "factory"
    RETAIL = "retail"
    ENTREPRENEUR = "entrepreneur"

    TYPE_SELLER_CHOICE = [
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "Индивидуальный предприниматель"),
    ]

    HIERARCHY_LEVELS = [
        (0, "Уровень 0"),
        (1, "Уровень 1"),
        (2, "Уровень 2"),
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
    product = models.ForeignKey(
        "retail.Product",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Товар",
        help_text="Укажите товар",
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Поставщик",
        help_text="Укажите поставщика",
    )
    debt = models.DecimalField(
        default=0.00,
        max_digits=11,
        decimal_places=2,
        verbose_name="Задолженность перед поставщиком",
        help_text="Укажите задолженность перед поставщиком",
    )
    creation_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        help_text="Укажите время создания",
    )
    hierarchy_level = models.IntegerField(
        default=0,
        choices=HIERARCHY_LEVELS,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(2)
        ],
        verbose_name="Уровень иерархии",
        help_text="Укажите уровень иерархии",
    )

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    def __str__(self):
        return f"{self.seller_title} - {self.seller_type}"
