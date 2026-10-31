# Django-go

Учебный проект интернет-магазина на Django.

Проект развивается поэтапно в рамках домашних работ курса.

## Домашняя работа 29

В рамках домашней работы в проект добавлено кеширование с использованием Redis, реализован сервисный слой для получения продуктов по категории и настроено кеширование отдельных страниц и результатов запросов.

## Реализовано

### Redis

- установлен и настроен Redis-совместимый сервер;
- в проект добавлена Python-библиотека `redis`;
- Django настроен для использования Redis в качестве backend кеширования;
- используется база Redis №1;
- соединение с Redis проверено командой `PING`;
- Redis успешно возвращает `PONG`.

Настройка кеша:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

## Кеширование страницы продукта

Детальная страница продукта кешируется на 15 минут.

Для кеширования используется Django `cache_page`.

Время кеширования:

```python
CACHE_TIMEOUT = 60 * 15
```

## Сервисный слой

В приложении `catalog` создан файл:

```text
catalog/services.py
```

Реализована сервисная функция:

```python
get_products_by_category(category_id)
```

Функция:

- принимает ID категории;
- формирует ключ кеша `category_{id}`;
- проверяет наличие списка продуктов в Redis;
- при наличии данных возвращает их из кеша;
- при отсутствии данных получает продукты из PostgreSQL;
- сохраняет результат в Redis;
- возвращает список продуктов выбранной категории.

## Низкоуровневое кеширование

Для списка товаров категории используется низкоуровневое кеширование через:

```python
cache.get()
cache.set()
```

Ключ формируется по шаблону:

```text
category_{id}
```

Время хранения данных составляет 15 минут.

Работа кеша была проверена через Redis CLI.

Пример ключа:

```text
:1:category_1
```

Пример проверки TTL:

```text
TTL :1:category_1
```

Redis возвращает положительное значение TTL, подтверждая наличие и срок жизни кеша.

## Страница товаров категории

Реализовано отдельное представление:

```python
CategoryProductListView
```

И отдельный шаблон:

```text
templates/category_products.html
```

Маршрут:

```text
/categories/<int:category_id>/
```

На странице отображаются все товары выбранной категории.

## Инвалидация кеша

При изменении данных кеш очищается или обновляется.

Очистка выполняется при:

- создании продукта;
- редактировании продукта;
- удалении продукта;
- снятии продукта с публикации.

Это позволяет избежать отображения устаревших данных.

## Основные файлы

```text
catalog/
├── forms.py
├── models.py
├── services.py
├── urls.py
└── views.py

templates/
├── category_products.html
├── product_confirm_delete.html
├── product_detail.html
├── product_form.html
├── home.html
└── ...
```

## Основные маршруты

Главная страница:

```text
/
```

Детальная страница продукта:

```text
/products/<int:pk>/
```

Создание продукта:

```text
/products/create/
```

Редактирование продукта:

```text
/products/<int:pk>/edit/
```

Удаление продукта:

```text
/products/<int:pk>/delete/
```

Товары выбранной категории:

```text
/categories/<int:category_id>/
```

## PostgreSQL

Подключение к базе данных настраивается через файл `.env`.

Пример:

```env
DATABASE_NAME=django_shop
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Файл `.env` не добавляется в репозиторий.

## Установка

Для управления зависимостями используется Poetry.

```bash
poetry install
```

## Redis

Redis должен быть запущен локально на порту:

```text
6379
```

Проверка:

```bash
memurai-cli ping
```

Ожидаемый ответ:

```text
PONG
```

## Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## Запуск проекта

```bash
python manage.py runserver
```

После запуска проект доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Проверка проекта

```bash
python manage.py check
```

Форматирование и проверка качества кода:

```bash
python -m isort .
black .
flake8 .
python -m isort --check-only .
black --check .
mypy .
```
