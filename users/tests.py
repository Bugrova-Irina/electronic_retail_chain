from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тестирование CRUD пользователя"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            is_active=True,
        )
        self.user.set_password("12345")
        self.user.save()

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        # Проверяем создание пользователя
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "is_active": True,
            "password": "12345",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
