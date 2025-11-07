from rest_framework import serializers

from retail.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Продавца"""

    class Meta:
        model = Seller
        fields = "__all__"
