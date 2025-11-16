# Торговая сеть электроники с иерархической структурой поставщиков на DjangoRestFramework
```python manage.py runserver``` - запуск веб-приложения. Ctrl+C - остановка сервера.

```python manage.py createsuperadmin```- создание суперпользователя, логин и пароль задаете сами.

```python manage.py createadmin```- создание суперпользователя с логином и паролем по умолчанию.

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
- SellerProduct (Связь между продавцом и товаром) - связывает продавца, товар и поставщика,
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
- Регистрация нового пользователя
```
POST /users/register/
{
    "email": "user@example.com",
    "password": "password"
}
```
- Аутентификация
```
POST /users/login/
{
    "email": "user@example.com",
    "password": "password"
}
```
- CRUD для Seller, Product, SellerProduct. Для поставщиков используется CRUD для Seller
  (создание, просмотр детальной информации поставщика, обновление, удаление, т.к. поставщик - 
это продавец с поставками товаров) и только для списка поставщиков создан отдельный эндпоинт.
- По ссылке http://127.0.0.1:8000/retail/ доступен список продавцов (заводов, розничных
магазинов, ИП).
- По ссылке http://127.0.0.1:8000/retail/products/ доступен список товаров.
- По ссылке http://127.0.0.1:8000/retail/seller-product/ доступен список связей между 
товарами и продавцами.
- По ссылке http://127.0.0.1:8000/retail/suppliers/ доступен список поставщиков.

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

В качестве базы данных используется PostgreSQL.
Установите Docker.

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
GET http://127.0.0.1:8000/retail/?country=Россия
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
Фильтрация поставщиков по стране:
```
GET http://127.0.0.1:8000/retail/suppliers/?country=Россия
```
Фильтрация по типу поставщика:
```
GET http://127.0.0.1:8000/retail/suppliers/?supplier_type=factory
```
Поиск поставщиков:
```
GET http://127.0.0.1:8000/retail/suppliers/?search=Electro
```
Сортировка:
```
GET http://127.0.0.1:8000/retail/suppliers/?ordering=-supplied_products_count
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
Запустите приложение
```
docker-compose up --build -d
```
Убедитесь, что все контейнеры запущены:
```
docker-compose ps
```
Оба контейнера (backend и db) должны быть в состоянии Up.

Автоматическое создание суперпользователя:
- При первом запуске автоматически создается суперпользователь:
  - Email: admin@example.com
  - Пароль: admin123

#### Проверка работы приложения:

1. Административная панель Django.
* URL: http://localhost:8080/admin/
* Учетные данные: admin@example.com / admin123
2. API эндпоинты.

Требуется аутентификация (JWT токен)

Получение токена доступа:
```
curl -X POST http://localhost:8080/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```
#### Импорт тестовых данных для проверки работы приложения
Загрузка данных отдельно для приложения retail, отдельно для users.
```
docker-compose exec backend python manage.py loaddata retail_data.json
docker-compose exec backend python manage.py loaddata users_data.json
```
Или сразу все данные для обоих приложений.
```
docker-compose exec backend python manage.py loaddata all_data.json
```

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