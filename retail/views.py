from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from retail.models import Seller
from retail.pagination import CustomPagination
from retail.serializers import SellerSerializer


class RetailCreateAPIView(CreateAPIView):
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
