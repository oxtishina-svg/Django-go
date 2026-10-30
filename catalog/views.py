from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Product


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу со списком товаров."""
    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Отображает страницу контактов."""
    return render(request, "contacts.html")


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Отображает подробную информацию о товаре."""
    product = get_object_or_404(Product, pk=pk)

    context = {
        "product": product,
    }

    return render(request, "product_detail.html", context)
