from typing import cast

from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import UserRegisterForm
from users.models import User


class RegisterView(FormView):
    """Регистрирует нового пользователя."""

    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        user = cast(User, form.save())

        login(
            self.request,
            user,
        )

        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию в нашем интернет-магазине.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)
