from django.contrib import admin

from retail.models import Product, Seller, SellerProduct


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("seller_title", "seller_type", "email", "city")
    list_filter = ("city",)
    search_fields = ("seller_title", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_title", "product_model", "product_launch_date")
    list_filter = ("product_title",)
    search_fields = ("product_title", "product_model")


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ("seller", "product", "selling_price", "quantity", "supplier", "debt")
    list_filter = ("quantity", "supplier", "debt")
    search_fields = ("supplier",)
