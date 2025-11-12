from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from retail.models import Product, Seller, SellerProduct
from retail.pagination import CustomPagination
from retail.serializers import (ProductSerializer, SellerProductSerializer,
                                SellerSerializer)


class SellerCreateAPIView(CreateAPIView):
    """Создание продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)


class SellerListAPIView(ListAPIView):
    """Вывод списка продавцов"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]  # Фильтрация по точному совпадению страны
    search_fields = ["seller_title", "city"]  # Поиск по названию и городу
    ordering_fields = ["seller_title", "creation_time"]  # Сортировка
    ordering = ["seller_title"]  # Сортировка по умолчанию


class SellerRetrieveAPIView(RetrieveAPIView):
    """Вывод информации о продавце"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)


class SellerUpdateAPIView(UpdateAPIView):
    """Обновление продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)


class SellerDestroyAPIView(DestroyAPIView):
    """Удаление продавца"""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)


class ProductCreateAPIView(CreateAPIView):
    """Создание продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductListAPIView(ListAPIView):
    """Вывод списка продавцов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


class ProductRetrieveAPIView(RetrieveAPIView):
    """Вывод информации о продавце"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductUpdateAPIView(UpdateAPIView):
    """Обновление продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductDestroyAPIView(DestroyAPIView):
    """Удаление продавца"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class SellerProductCreateAPIView(CreateAPIView):
    """Создание cвязи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    permission_classes = (IsAuthenticated,)


class SellerProductListAPIView(ListAPIView):
    """Вывод списка связей продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


class SellerProductRetrieveAPIView(RetrieveAPIView):
    """Вывод информации о связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    permission_classes = (IsAuthenticated,)


class SellerProductUpdateAPIView(UpdateAPIView):
    """Обновление связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    permission_classes = (IsAuthenticated,)


class SellerProductDestroyAPIView(DestroyAPIView):
    """Удаление связи продавец-товар"""
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer
    permission_classes = (IsAuthenticated,)
