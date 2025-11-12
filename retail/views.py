from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from retail.mixins import ActiveEmployeePermissionMixin
from retail.models import Product, Seller, SellerProduct
from retail.pagination import CustomPagination
from retail.serializers import (ProductSerializer, SellerProductSerializer,
                                SellerSerializer)


class SellerCreateAPIView(ActiveEmployeePermissionMixin, CreateAPIView):
    """Создание продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerListAPIView(ActiveEmployeePermissionMixin, ListAPIView):
    """Вывод списка продавцов"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]  # Фильтрация по точному совпадению страны
    search_fields = ["seller_title", "city"]  # Поиск по названию и городу
    ordering_fields = ["seller_title", "creation_time"]  # Сортировка
    ordering = ["seller_title"]  # Сортировка по умолчанию


class SellerRetrieveAPIView(ActiveEmployeePermissionMixin, RetrieveAPIView):
    """Вывод информации о продавце"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerUpdateAPIView(ActiveEmployeePermissionMixin, UpdateAPIView):
    """Обновление продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerDestroyAPIView(ActiveEmployeePermissionMixin, DestroyAPIView):
    """Удаление продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class ProductCreateAPIView(ActiveEmployeePermissionMixin, CreateAPIView):
    """Создание продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListAPIView(ActiveEmployeePermissionMixin, ListAPIView):
    """Вывод списка продавцов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class ProductRetrieveAPIView(ActiveEmployeePermissionMixin, RetrieveAPIView):
    """Вывод информации о продавце"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(ActiveEmployeePermissionMixin, UpdateAPIView):
    """Обновление продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDestroyAPIView(ActiveEmployeePermissionMixin, DestroyAPIView):
    """Удаление продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SellerProductCreateAPIView(ActiveEmployeePermissionMixin, CreateAPIView):
    """Создание cвязи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer


class SellerProductListAPIView(ActiveEmployeePermissionMixin, ListAPIView):
    """Вывод списка связей продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    pagination_class = CustomPagination


class SellerProductRetrieveAPIView(ActiveEmployeePermissionMixin, RetrieveAPIView):
    """Вывод информации о связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer


class SellerProductUpdateAPIView(ActiveEmployeePermissionMixin, UpdateAPIView):
    """Обновление связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer


class SellerProductDestroyAPIView(ActiveEmployeePermissionMixin, DestroyAPIView):
    """Удаление связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
