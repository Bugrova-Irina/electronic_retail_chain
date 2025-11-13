from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from retail.models import Product, Seller, SellerProduct


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = [
        "seller_title",
        "seller_type",
        "email",
        "country",
        "city",
        "supplier_link",
        "creation_time",
    ]
    list_filter = ["seller_type", "city", "country", "creation_time"]
    search_fields = ["seller_title", "email", "city", "country"]
    readonly_fields = ["creation_time"]
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("seller_title", "seller_type", "email", "creation_time")},
        ),
        ("Адрес", {"fields": ("country", "city", "street", "house_number")}),
    )

    def supplier_link(self, obj):
        """Ссылка на поставщика"""
        supplier_products = SellerProduct.objects.filter(seller=obj)
        if supplier_products.exists():
            suppliers = []
            for seller_product in supplier_products[
                :5
            ]:  # Показываем первых 5 поставщиков
                url = reverse(
                    "admin:retail_seller_change", args=[seller_product.supplier.id]
                )
                suppliers.append(
                    f'<a href="{url}">{seller_product.supplier.seller_title}</a>'
                )
            return format_html(", ".join(suppliers))
        return "Нет поставщиков"

    supplier_link.short_description = "Поставщики"
    supplier_link.allow_tags = True

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("sellerproduct_set__supplier")
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_title",
        "product_model",
        "manufacturer",
        "product_launch_date",
    ]
    list_filter = ["manufacturer", "product_launch_date"]
    search_fields = ["product_title", "product_model", "description"]
    raw_id_fields = ["manufacturer"]


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_editable = ["debt"]  # Разрешаем редактировать задолженность прямо в таблице
    list_display = [
        "id",
        "seller_link",
        "product_link",
        "supplier_link",
        "selling_price",
        "quantity",
        "debt",
        "hierarchy_level",
        "clear_debt_button",
    ]
    list_filter = [
        "seller__city",
        "seller__country",
        "hierarchy_level",
        "seller__seller_type",
    ]
    search_fields = [
        "seller__seller_title",
        "product__product_title",
        "supplier__seller_title",
    ]
    readonly_fields = ["hierarchy_level"]
    actions = ["clear_debt_action"]

    # Добавляем поля для формы редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("seller", "product", "supplier")}),
        ("Торговая информация", {"fields": ("selling_price", "quantity", "debt")}),
        ("Системная информация", {"fields": ("hierarchy_level",)}),
    )

    # Добавляем кастомную кнопку очистки долга в список
    def clear_debt_button(self, obj):
        if obj.debt > 0:
            url = reverse("admin:retail_sellerproduct_clear_debt", args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background: #dc3545; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; border: none; display: inline-block;">Очистить долг</a>',
                url,
            )
        else:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">Нет долга</span>'
            )

    clear_debt_button.short_description = "Управление долгом"
    clear_debt_button.allow_tags = True

    # Ссылки на связанные объекты
    def seller_link(self, obj):
        url = reverse("admin:retail_seller_change", args=[obj.seller.id])
        return format_html('<a href="{}">{}</a>', url, obj.seller.seller_title)

    seller_link.short_description = "Продавец"
    seller_link.admin_order_field = "seller__seller_title"

    def product_link(self, obj):
        url = reverse("admin:retail_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.product_title)

    product_link.short_description = "Товар"
    product_link.admin_order_field = "product__product_title"

    def supplier_link(self, obj):
        url = reverse("admin:retail_seller_change", args=[obj.supplier.id])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.seller_title)

    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = "supplier__seller_title"

    # Отображение долга с цветом
    def debt_display(self, obj):
        color = "#dc3545" if obj.debt > 0 else "#28a745"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>', color, obj.debt
        )

    debt_display.short_description = "Задолженность"

    # Admin action для очистки задолженности
    @admin.action(description="Очистить задолженность у выбранных записей")
    def clear_debt_action(self, request, queryset):
        updated_count = queryset.update(debt=0.00)
        self.message_user(
            request,
            f"Задолженность очищена у {updated_count} записей.",
            messages.SUCCESS,
        )

    # Кастомный URL для очистки долга одной записи
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/clear-debt",
                self.admin_site.admin_view(self.clear_debt_view),
                name="retail_sellerproduct_clear_debt",
            ),
        ]
        return custom_urls + urls

    def clear_debt_view(self, request, object_id):
        """Представление для очистки долга одной записи"""
        try:
            obj = self.get_queryset(request).get(pk=object_id)
            obj.debt = 0.00
            obj.save()
            self.message_user(
                request, f"Задолженность для '{obj}' очищена.", messages.SUCCESS
            )
        except SellerProduct.DoesNotExist:
            self.message_user(request, "Запись не найдена.", messages.ERROR)

        # Возвращаемся к списку записей
        return HttpResponseRedirect("../../")

    # Для оптимизации запросов
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("seller", "product", "supplier")
        )
