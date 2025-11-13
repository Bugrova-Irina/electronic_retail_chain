from http.client import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from retail.models import Seller, SellerProduct, Product
from users.models import User


class SellerTestCase(APITestCase):
    """Тестирование CRUD продавцов"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            is_active=True
        )
        # Экземпляр продавца
        self.seller = Seller.objects.create(
            seller_title="Factory 1",
            seller_type="factory",
            email="factory1@test.com",
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_seller_create(self):
        # Проверяем создание продавца
        url = reverse("retail:seller-create")
        data = {
            "seller_title": "retail1",
            "seller_type": "retail",
            "email": "retail@test.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seller.objects.all().count(), 2)

    def test_seller_retrieve(self):
        # Проверяем вывод информации о продавце
        url = reverse("retail:seller-detail", args=(self.seller.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("seller_title"), self.seller.seller_title)

    def test_seller_update(self):
        # Проверяем обновление информации о продавце
        url = reverse("retail:seller-update", args=(self.seller.pk,))
        data = {"seller_title": "factory 11"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("seller_title"), "factory 11")

    def test_seller_delete(self):
        # Проверяем удаление продавца
        url = reverse("retail:seller-delete", args=(self.seller.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seller.objects.all().count(), 0)

    def test_seller_list(self):
        # Проверяем вывод списка продавцов
        url = reverse("retail:sellers")
        response = self.client.get(url)
        data = response.json()

        # Используем динамические ID вместо хардкода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        seller_data = data["results"][0]
        self.assertEqual(seller_data["seller_title"], self.seller.seller_title)
        self.assertEqual(seller_data["seller_type"], self.seller.seller_type)
        self.assertEqual(seller_data["email"], self.seller.email)


class ProductTestCase(APITestCase):
    """Тестирование CRUD товара"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            is_active=True
        )
        # Экземпляр продавца
        self.seller = Seller.objects.create(
            seller_title="Factory 1",
            seller_type="factory",
            email="factory1@test.com",
        )
        # Экземпляр товара
        self.product = Product.objects.create(
            product_title="Product 1",
            product_model="Model 1",
            manufacturer=self.seller,
            product_launch_date="2025-10-15",
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_product_create(self):
        # Проверяем создание товара
        url = reverse("retail:product-create")
        data = {
            "product_title": "Product 2",
            "product_model": "Model 2",
            "manufacturer": self.seller.id,
            "product_launch_date": "2025-10-15",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_retrieve(self):
        # Проверяем вывод информации о товаре
        url = reverse("retail:product-detail", args=(self.product.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("product_title"), self.product.product_title)

    def test_product_update(self):
        # Проверяем обновление информации о товаре
        url = reverse("retail:product-update", args=(self.product.pk,))
        data = {"product_title": "Product 21"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("product_title"), "Product 21")

    def test_product_delete(self):
        # Проверяем удаление товара
        url = reverse("retail:product-delete", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_list(self):
        # Проверяем вывод списка товаров
        url = reverse("retail:products")
        response = self.client.get(url)
        data = response.json()

        # Используем динамические ID вместо хардкода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        product_data = data["results"][0]
        self.assertEqual(product_data["product_title"], self.product.product_title)
        self.assertEqual(product_data["product_model"], self.product.product_model)
        self.assertEqual(product_data["manufacturer"], self.product.manufacturer.id)


class SellerProductTestCase(APITestCase):
    """Тестирование CRUD связи продавца с товаром"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            is_active=True
        )
        # Экземпляр продавца
        self.seller = Seller.objects.create(
            seller_title="Factory 1",
            seller_type="factory",
            email="factory1@test.com",
        )
        # Экземпляр поставщика
        self.supplier = Seller.objects.create(
            seller_title="Factory 2",
            seller_type="factory",
            email="factory2@test.com",
        )
        # Экземпляр товара
        self.product = Product.objects.create(
            product_title="Product 1",
            product_model="Model 1",
            manufacturer=self.supplier,
            product_launch_date="2025-10-15",
        )
        # Экземпляр связи продавца с товаром
        self.sellerproduct = SellerProduct.objects.create(
            seller=self.seller,
            product=self.product,
            selling_price=100.00,
            quantity=10,
            supplier=self.supplier
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_seller_product_create(self):
        # Проверяем создание связи продавца с товаром
        # Создаем новый товар для новой связи
        new_product = Product.objects.create(
            product_title="Product 2",
            product_model="Model 2",
            manufacturer=self.supplier,
            product_launch_date="2025-10-15",
        )
        url = reverse("retail:seller-product-create")
        data = {
            "seller": self.seller.id,
            "product": new_product.id,  # Используем новый товар
            "selling_price": "150.15",
            "quantity": 15,
            "supplier": self.supplier.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SellerProduct.objects.all().count(), 2)

    def test_seller_product_retrieve(self):
        # Проверяем вывод информации о связи продавца с товаром
        url = reverse("retail:seller-product-detail", args=(self.sellerproduct.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("seller"), self.seller.id)

    def test_seller_product_update(self):
        # Проверяем обновление информации о связи продавца с товаром
        url = reverse("retail:seller-product-update", args=(self.sellerproduct.pk,))
        data = {"quantity": 20}
        response = self.client.patch(url, data)

        if response.status_code != status.HTTP_200_OK:
            print(f"Update error: {response.json()}")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("quantity"), 20)

    def test_seller_product_delete(self):
        # Проверяем удаление связи продавца с товаром
        url = reverse("retail:seller-product-delete", args=(self.sellerproduct.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SellerProduct.objects.all().count(), 0)

    def test_seller_product_list(self):
        # Проверяем вывод списка связей продавца с товаром
        url = reverse("retail:seller-product-list")
        response = self.client.get(url)
        data = response.json()

        # Используем динамические ID вместо хардкода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        product_data = data["results"][0]
        self.assertEqual(product_data["seller"], self.sellerproduct.seller.id)
        self.assertEqual(product_data["product"], self.sellerproduct.product.id)
        self.assertEqual(float(product_data["selling_price"]), float(self.sellerproduct.selling_price))
        self.assertEqual(product_data["quantity"], self.sellerproduct.quantity)
        self.assertEqual(product_data["supplier"], self.sellerproduct.supplier.id)

    def test_seller_product_self_supplier_validation(self):
        """Проверка валидации, когда продавец является своим собственным поставщиком"""
        url = reverse("retail:seller-product-create")
        data = {
            "seller": self.seller.id,
            "product": self.product.id,
            "selling_price": "150.15",
            "quantity": 15,
            "supplier": self.seller.id  # Нарушение валидации
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
