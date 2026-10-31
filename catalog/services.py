from typing import cast

from django.core.cache import cache

from catalog.models import Product

CACHE_TIMEOUT = 60 * 15


def get_products_by_category(category_id: int) -> list[Product]:
    """Возвращает товары категории с использованием кеша."""

    cache_key = f"category_{category_id}"

    products = cast(
        list[Product] | None,
        cache.get(cache_key),
    )

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
            )
        )

        cache.set(
            cache_key,
            products,
            CACHE_TIMEOUT,
        )

    return products
