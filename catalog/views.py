from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу."""
    return render(request, "home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """Отображает страницу контактов."""
    return render(request, "contacts.html")
