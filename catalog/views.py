from typing import Any, cast

from django import forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Category, Product
from catalog.services import CACHE_TIMEOUT, get_products_by_category
from users.models import User


class ProductListView(ListView):
    """Отображает главную страницу со списком товаров."""

    model = Product
    template_name = "home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """Отображает страницу контактов."""

    template_name = "contacts.html"


@method_decorator(
    cache_page(CACHE_TIMEOUT),
    name="dispatch",
)
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

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        product_form = cast(ProductForm, form)
        product_form.instance.owner = cast(User, self.request.user)

        response = super().form_valid(form)

        product = cast(Product, self.object)
        cache.delete(f"category_{product.category_id}")

        return cast(HttpResponse, response)

    def get_success_url(self) -> str:
        product = cast(Product, self.object)

        return reverse(
            "catalog:product_detail",
            kwargs={"pk": product.pk},
        )


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """Редактирует продукт."""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    raise_exception = True

    def test_func(self) -> bool:
        product = cast(Product, self.get_object())

        return bool(product.owner == self.request.user)

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        old_product = cast(Product, self.get_object())
        old_category_id = old_product.category_id

        response = super().form_valid(form)

        product = cast(Product, self.object)

        cache.clear()
        cache.delete(f"category_{old_category_id}")
        cache.delete(f"category_{product.category_id}")

        return cast(HttpResponse, response)

    def get_success_url(self) -> str:
        product = cast(Product, self.object)

        return reverse(
            "catalog:product_detail",
            kwargs={"pk": product.pk},
        )


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    """Удаляет продукт."""

    model = Product
    template_name = "product_confirm_delete.html"
    raise_exception = True

    def test_func(self) -> bool:
        product = cast(Product, self.get_object())

        is_owner = bool(product.owner == self.request.user)
        is_moderator = bool(self.request.user.has_perm("catalog.delete_product"))

        return is_owner or is_moderator

    def form_valid(self, form: forms.Form) -> HttpResponse:
        product = cast(Product, self.object)

        cache.clear()
        cache.delete(f"category_{product.category_id}")

        return cast(
            HttpResponse,
            super().form_valid(form),
        )

    def get_success_url(self) -> str:
        return reverse("catalog:home")


class ProductUnpublishView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    """Снимает продукт с публикации."""

    permission_required = "catalog.can_unpublish_product"
    raise_exception = True

    def post(
        self,
        request: HttpRequest,
        pk: int,
    ) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)

        product.is_published = False
        product.save(update_fields=["is_published"])

        cache.clear()
        cache.delete(f"category_{product.category_id}")

        return redirect(
            "catalog:product_detail",
            pk=product.pk,
        )


class CategoryProductListView(TemplateView):
    """Отображает товары выбранной категории."""

    template_name = "category_products.html"

    def get_context_data(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        category_id = int(self.kwargs["category_id"])

        context["category"] = get_object_or_404(
            Category,
            pk=category_id,
        )
        context["products"] = get_products_by_category(
            category_id,
        )

        return context
