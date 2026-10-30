# Django-go

Учебный проект интернет-магазина на Django.

Проект создается поэтапно в рамках домашних работ курса и будет расширяться по мере изучения Django.

## Домашняя работа 22.3

В рамках домашней работы создан и настроен базовый Django-проект и приложение `catalog`.

### Реализовано

- создан Django-проект;
- создано приложение `catalog`;
- приложение зарегистрировано в `INSTALLED_APPS`;
- настроена маршрутизация проекта;
- создан отдельный `urls.py` приложения `catalog`;
- маршруты приложения подключены через `include`;
- создан контроллер главной страницы;
- создан контроллер страницы контактов;
- контроллеры используют функцию `render`;
- главная страница доступна по адресу `/`;
- страница контактов доступна по адресу `/contacts/`;
- все URL заканчиваются символом `/`;
- созданы HTML-шаблоны главной страницы и страницы контактов;
- для стилизации используется Bootstrap.

## Структура Django-проекта

```text
catalog/
├── migrations/
│   └── __init__.py
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

templates/
├── contacts.html
└── home.html

manage.py
```

## Установка

Для управления зависимостями используется Poetry.

```bash
poetry install
```

Если Poetry не добавлен в PATH на Windows:

```powershell
& "$env:APPDATA\Python\Scripts\poetry.exe" install
```

## Запуск проекта

```bash
python manage.py runserver
```

После запуска проект доступен по адресу:

```text
http://127.0.0.1:8000/
```

Страница контактов:

```text
http://127.0.0.1:8000/contacts/
```

Административная панель Django:

```text
http://127.0.0.1:8000/admin/
```

## Проверка проекта

Проверка конфигурации Django:

```bash
python manage.py check
```

Форматирование и проверка качества Python-кода:

```bash
python -m isort .
black .
flake8 .
python -m isort --check-only .
black --check .
mypy .
```
