from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):
    """Отображает главную страницу со списком товаров."""

    model = Product
    template_name = "home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """Отображает страницу контактов."""

    template_name = "contacts.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает подробную информацию о товаре."""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создаёт новый продукт."""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def get_success_url(self) -> str:
        product = cast(Product, self.object)

        return reverse(
            "catalog:product_detail",
            kwargs={"pk": product.pk},
        )


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует существующий продукт."""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def get_success_url(self) -> str:
        product = cast(Product, self.object)

        return reverse(
            "catalog:product_detail",
            kwargs={"pk": product.pk},
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет продукт."""

    model = Product
    template_name = "product_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("catalog:home")
