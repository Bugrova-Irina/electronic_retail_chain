from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователя"""

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},  # Пароль не должен возвращаться в ответах
            "is_active": {"read_only": True},
        }
