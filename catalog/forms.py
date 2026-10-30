from decimal import Decimal
from typing import Any, cast

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
            "is_published",
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update(
                    {
                        "class": "form-check-input",
                    }
                )
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                    }
                )

            if field_name == "name":
                field.widget.attrs.update(
                    {
                        "placeholder": "Введите название товара",
                    }
                )

            elif field_name == "description":
                field.widget.attrs.update(
                    {
                        "placeholder": "Введите описание товара",
                    }
                )

            elif field_name == "price":
                field.widget.attrs.update(
                    {
                        "placeholder": "Введите цену товара",
                    }
                )

    def clean_name(self) -> str:
        """Проверяет название на запрещённые слова."""
        name = cast(str, self.cleaned_data.get("name", ""))
        name_lower = name.lower()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in name_lower:
                raise ValidationError(f'Название продукта не может содержать запрещённое слово "{forbidden_word}".')

        return name

    def clean_description(self) -> str:
        """Проверяет описание на запрещённые слова."""
        description = cast(
            str,
            self.cleaned_data.get("description", ""),
        )
        description_lower = description.lower()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in description_lower:
                raise ValidationError(f'Описание продукта не может содержать запрещённое слово "{forbidden_word}".')

        return description

    def clean_price(self) -> Decimal | None:
        """Проверяет, что цена продукта не отрицательная."""
        price = cast(
            Decimal | None,
            self.cleaned_data.get("price"),
        )

        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")

        return price
