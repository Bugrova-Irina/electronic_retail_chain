from django.contrib import admin

from retail.models import Seller, Product


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("seller_title", "seller_type", "email", "supplier", "city", "debt")
    list_filter = ("city",)
    search_fields = ("seller_title", "supplier", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_title", "product_model", "price", "product_launch_date")
    list_filter = ("product_title", "price")
    search_fields = ("product_title", "product_model")
