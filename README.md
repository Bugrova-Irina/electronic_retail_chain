# Торговая сеть электроники на DjangoRestFramework
```python manage.py runserver``` - запуск веб-приложения. Ctrl+C - остановка сервера.

```python manage.py createsuperadmin``` - создание суперпользователя

```python manage.py test``` - запуск тестов

## Описание:

Веб-приложение с API-интерфейсом и админ-панелью с сохранением данных в базу данных.

Сеть представляет собой иерархическую структуру из трех уровней:
- завод (уровень 0),
- розничная сеть,
- индивидуальный предприниматель.

У покупателей может быть задолженность перед поставщиком по каждому товару в отдельности.
Для каждого покупателя автоматически подсчитывается общая задолженность по всем товарам. Ее
можно увидеть в списке продавцов http://127.0.0.1:8000/retail/ в поле total_debt для каждого
продавца как в админ-панели, так и в соответствующем эндпоинте.

Только активные пользователи (is_active=True) имеют доступ к API. Задолженность нельзя изменить
через API. Очистка или изменение значения задолженности настроено только в админ-панели.

В приложении настроена дополнительная валидация:
* Производителем товара может быть только завод или ИП.
* Продавец не может быть своим поставщиком.
* Уникальность связей (seller + product + supplier).

### Как работает иерархия:

- При создании связи SellerProduct автоматически вычисляется hierarchy_level.
- Если поставщик - завод → уровень 1.
- Если поставщик не завод → уровень = (уровень поставщика + 1).
- Если у поставщика нет этого товара → уровень 1.

**Пример:**
Завод A (уровень 0) → Розница B (уровень 1) → ИП C (уровень 2)

### Приложение использует 4 модели:

- Seller (Продавец) - основная информация о продавце.
- Product (Товар) - основная информация о товаре.
- SellerProduct(Связь между продавцом и товаром) - связывает продавца, товар и поставщика,
хранит цену, количество, задолженность, автоматически вычисляет уровень иерархии.
- User (Пользователь приложения).

### Админ-панель
SellerAdmin:

* Ссылки на поставщиков в списке.
* Фильтр по городу (list_filter = ["city"]).
* Поиск по названию и городу.
* Отображение поставщиков через supplier_link.

ProductAdmin:

* Стандартный CRUD для товаров.
* Фильтрация по производителю.

SellerProductAdmin:

* Активные ссылки на продавцов, товары, поставщиков.
* Фильтр по городу через seller__city.
* Admin action для массовой очистки задолженности.
* Индивидуальные кнопки очистки долга для каждой записи.
* Редактирование долга в списке (list_editable = ["debt"]).

### API Эндпоинты
- Аутентификация

```
POST /users/login/
{
    "email": "user@example.com",
    "password": "password"
}
```
- CRUD для Seller, Product, SellerProduct
- По ссылке http://127.0.0.1:8000/retail/ доступен список продавцов (заводов, розничных
магазинов, ИП).
- По ссылке http://127.0.0.1:8000/retail/products/ доступен список товаров.
- По ссылке http://127.0.0.1:8000/retail/seller-product/ доступен список связей между 
товарами и продавцами.

## Требования к окружению:

Установите:
 - python 3.13.0
 - Poetry
 - Django
 - Pillow
 - python-dotenv
 - psycopg2 или psycopg2-binary
 - djangorestframework
 - djangorestframework-simplejwt
 - flake8
 - black
 - isort
 - coverage
 - drf-yasg
 - django-filter

В качестве базы данных используется PostgreSQL

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/Bugrova-Irina/electronic_retail_chain/
```

2. Установите зависимости:
```
poetry shell
```
```
poetry add django
```
```
poetry add Pillow
```
```
poetry add psycopg2
```
```
poetry add python-dotenv
```
```
poetry add djangorestframework
```
```
poetry add djangorestframework-simplejwt
```
```
poetry add flake8
```
```
poetry add black
```
```
poetry add isort
```
```
poetry add coverage
```
```
poetry add drf-yasg
```
```
poetry add django-filter
```

3. Создайте файл `.env` на основе `.env.sample`
4. Заполните переменные окружения в `.env` файле.

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/retail/.

### Фильтрация и поиск в API
Фильтрация продавцов по стране:
```
GET http://127.0.0.1:8000/retail/?country=Russia
```
Поиск:
```
GET http://127.0.0.1:8000/retail/?search=Tech
GET http://127.0.0.1:8000/retail/?search=Moscow
```
Сортировка:
```
GET http://127.0.0.1:8000/retail/?ordering=seller_title          # по возрастанию
GET http://127.0.0.1:8000/retail/?ordering=-creation_time        # по убыванию
GET http://127.0.0.1:8000/retail/?ordering=city,-seller_title    # комбинированная
```
Пагинация:
```
GET http://127.0.0.1:8000/retail/?page=2
GET http://127.0.0.1:8000/retail/?page_size=10
```

### Создание цепочки поставок
1. Создаем завод
```
POST http://127.0.0.1:8000/retail/create/
{
    "seller_title": "ElectroFactory",
    "seller_type": "factory",
    "email": "factory@example.com",
    "country": "Germany",
    "city": "Berlin"
}
```
2. Создаем товар
```
POST http://127.0.0.1:8000/retail/product/create/
{
    "product_title": "Smartphone X10",
    "product_model": "X10",
    "manufacturer": 1,
    "product_launch_date": "2024-01-15"
}
```
3. Создаем розничного продавца
```
POST http://127.0.0.1:8000/retail/create/
{
    "seller_title": "TechStore",
    "seller_type": "retail", 
    "email": "techstore@example.com",
    "country": "Russia",
    "city": "Moscow"
}
```
4. Создаем связь (розница покупает у завода)
```
POST http://127.0.0.1:8000/retail/seller-product/create/
{
    "seller": 2,
    "product": 1,
    "supplier": 1,
    "selling_price": "15000.00",
    "quantity": 50,
    "debt": "75000.00"
}
```

### Запуск проекта с использованием Docker Compose (для разработки):

#### Команды для запуска:
Выполните сборку образов:
```
docker-compose build
```

Запуск контейнеров в фоновом режиме:
```
docker-compose up -d
```

Убедитесь, что все контейнеры запущены:
```
docker-compose ps
```

Примените миграции базы данных:
```
docker-compose exec backend python manage.py migrate
```

Создайте учетную запись администратора
```
docker-compose exec web python manage.py createadmin
```

Проверка работы приложения:
Перейдите по адресу: http://localhost:8080/retail/

## Тестирование:

Добавлено тестирование корректности работы CRUD продавцов, товаров и связей между
продавцами и товарами. 

Добавлен отчет о покрытии тестами в папке htmlcov/index.html.

1. Запуск тестов с покрытием
```
coverage run --source='.' manage.py test
```
2. Генерация HTML отчета
```
coverage html
```
## Документация:

Для проекта подключен и настроен вывод документации с помощью drf-yasg.
```
http://127.0.0.1:8000/redoc/
```
```
http://127.0.0.1:8000/swagger/
```

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)