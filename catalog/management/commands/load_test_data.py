from pathlib import Path

from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    """Загружает тестовые данные из фикстуры."""

    help = "Загружает тестовые категории и продукты из фикстуры"

    def handle(self, *args: object, **options: object) -> None:
        Product.objects.all().delete()
        Category.objects.all().delete()

        base_dir = Path(__file__).resolve().parents[3]
        fixture_path = base_dir / "fixtures" / "catalog_data.json"

        call_command(
            "loaddata",
            str(fixture_path),
        )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены."))
