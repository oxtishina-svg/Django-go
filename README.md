# Django-go

Учебный проект интернет-магазина на Django.

Проект развивается поэтапно в рамках домашних работ курса.

## Домашняя работа 23

В рамках домашней работы проект переведен на PostgreSQL, добавлены модели товаров и категорий, настроена административная панель, работа через Django Shell, фикстуры и кастомная команда загрузки данных.

## Реализовано

- подключена PostgreSQL вместо SQLite;
- параметры подключения к базе данных вынесены в `.env`;
- создан шаблон `.env_template`;
- добавлены зависимости:
  - `psycopg2-binary`;
  - `python-dotenv`;
  - `Pillow`;
  - `IPython`;
- настроены `MEDIA_URL` и `MEDIA_ROOT`;
- реализованы модели `Category` и `Product`;
- модель `Product` связана с `Category` через `ForeignKey`;
- реализованы методы `__str__`;
- для моделей настроены параметры `Meta`;
- созданы и применены миграции;
- модели зарегистрированы в административной панели;
- настроены отображение, фильтрация и поиск в админке;
- создан суперпользователь;
- выполнена работа с данными через Django Shell;
- созданы категории и товары через ORM;
- выполнены запросы на получение, фильтрацию, обновление и удаление данных;
- добавлены скриншоты работы с Django Shell;
- сформирована фикстура для категорий и товаров;
- реализована кастомная management-команда для очистки базы и загрузки тестовых данных из фикстуры.

## Модели

### Category

Поля:

- `name` — наименование категории;
- `description` — описание категории.

### Product

Поля:

- `name` — наименование товара;
- `description` — описание;
- `image` — изображение;
- `category` — категория товара;
- `price` — цена;
- `created_at` — дата создания;
- `updated_at` — дата последнего изменения.

## Структура проекта

```text
catalog/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── load_test_data.py
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py

config/
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py

fixtures/
└── catalog_data.json

screenshots/
├── Screenshot_01.jpg
└── Screenshot_02.jpg

templates/
├── contacts.html
└── home.html

.env_template
manage.py
pyproject.toml
poetry.lock
README.md
```

## Переменные окружения

Для подключения к PostgreSQL используется файл `.env`.

Пример значений находится в `.env_template`:

```env
DATABASE_NAME=django_shop
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Файл `.env` не должен попадать в репозиторий.

## Установка

Для управления зависимостями используется Poetry.

```bash
poetry install
```

## Миграции

Создание миграций:

```bash
python manage.py makemigrations
```

Применение миграций:

```bash
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

Административная панель:

```text
http://127.0.0.1:8000/admin/
```

## Django Shell

Запуск:

```bash
python manage.py shell
```

В рамках домашней работы через ORM были выполнены операции:

- создание категорий;
- создание товаров;
- получение всех категорий;
- получение всех товаров;
- фильтрация товаров по категории;
- обновление цены товара;
- удаление товара.

Скриншоты выполнения команд находятся в директории:

```text
screenshots/
```

## Фикстуры

Фикстура находится в:

```text
fixtures/catalog_data.json
```

Загрузка данных:

```bash
python -X utf8 manage.py loaddata fixtures/catalog_data.json
```

## Кастомная команда

Для очистки текущих данных и загрузки тестовых данных из фикстуры используется команда:

```bash
python -X utf8 manage.py load_test_data
```

## Проверка проекта

Проверка Django:

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
