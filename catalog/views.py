from django.views.generic import DetailView, ListView, TemplateView

from catalog.models import Product


class ProductListView(ListView):
    """Отображает главную страницу со списком товаров."""

    model = Product
    template_name = "home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """Отображает страницу контактов."""

    template_name = "contacts.html"


class ProductDetailView(DetailView):
    """Отображает подробную информацию о товаре."""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
