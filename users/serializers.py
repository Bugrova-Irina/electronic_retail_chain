from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериалайзер для модели пользователя"""
    model = User
    fields = "__all__"
