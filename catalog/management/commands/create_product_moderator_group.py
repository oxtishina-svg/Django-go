from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создаёт группу модераторов продуктов и назначает ей права."""

    help = "Создаёт группу 'Модератор продуктов' и назначает необходимые права"

    def handle(self, *args: object, **options: object) -> None:
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов",
        )

        permissions = Permission.objects.filter(
            codename__in=[
                "can_unpublish_product",
                "delete_product",
            ]
        )

        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана."))
        else:
            self.stdout.write(self.style.WARNING("Группа 'Модератор продуктов' уже существует."))

        self.stdout.write(self.style.SUCCESS("Права группы обновлены."))
