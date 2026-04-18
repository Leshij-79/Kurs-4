import secrets

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserProfileForm
from users.models import CustomUser


def UserLogoutView(request):
    logout(request)
    return redirect("sending_mail:mailing_list")


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("sending_mail:mailing_list")


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class RegisterView(FormView):
    model = CustomUser
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("sending_mail:mailing_list")

    def form_valid(self, form):
        user = form.save()

        user.is_active = False
        token = secrets.token_hex(16)  # 16 - шкала чисел
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confurm/{token}/"
        send_mail(
            subject="Авторизация на сайте",
            message=f"Для завершения регистрации перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


class UserProfileView(UpdateView):
    model = CustomUser
    template_name = "profile.html"
    form_class = CustomUserProfileForm
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_object(self):
        return self.request.user
