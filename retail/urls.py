from django.urls import path

from retail.apps import RetailConfig
from retail.views import (ProductCreateAPIView, ProductDestroyAPIView,
                          ProductListAPIView, ProductRetrieveAPIView,
                          ProductUpdateAPIView, SellerCreateAPIView,
                          SellerDestroyAPIView, SellerListAPIView,
                          SellerProductCreateAPIView,
                          SellerProductDestroyAPIView,
                          SellerProductListAPIView,
                          SellerProductRetrieveAPIView,
                          SellerProductUpdateAPIView, SellerRetrieveAPIView,
                          SellerUpdateAPIView, SupplierListAPIView)

app_name = RetailConfig.name

urlpatterns = [
    path("", SellerListAPIView.as_view(), name="sellers"),
    path("<int:pk>/", SellerRetrieveAPIView.as_view(), name="seller-detail"),
    path("<int:pk>/update/", SellerUpdateAPIView.as_view(), name="seller-update"),
    path("create/", SellerCreateAPIView.as_view(), name="seller-create"),
    path("<int:pk>/delete/", SellerDestroyAPIView.as_view(), name="seller-delete"),
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("product/<int:pk>/", ProductRetrieveAPIView.as_view(), name="product-detail"),
    path(
        "product/<int:pk>/update/",
        ProductUpdateAPIView.as_view(),
        name="product-update",
    ),
    path("product/create/", ProductCreateAPIView.as_view(), name="product-create"),
    path(
        "product/<int:pk>/delete/",
        ProductDestroyAPIView.as_view(),
        name="product-delete",
    ),
    path(
        "seller-product/",
        SellerProductListAPIView.as_view(),
        name="seller-product-list",
    ),
    path(
        "seller-product/<int:pk>/",
        SellerProductRetrieveAPIView.as_view(),
        name="seller-product-detail",
    ),
    path(
        "seller-product/<int:pk>/update/",
        SellerProductUpdateAPIView.as_view(),
        name="seller-product-update",
    ),
    path(
        "seller-product/create/",
        SellerProductCreateAPIView.as_view(),
        name="seller-product-create",
    ),
    path(
        "seller-product/<int:pk>/delete/",
        SellerProductDestroyAPIView.as_view(),
        name="seller-product-delete",
    ),
    path(
        "suppliers/", SupplierListAPIView.as_view(), name="suppliers"
    ),
]
