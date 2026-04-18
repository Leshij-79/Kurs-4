import secrets

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserProfileForm, \
    CustomPasswordResetForm, CustomPasswordSetForm
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
        url = f"http://{host}/users/email-confirm/{token}/"
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


class UserPasswordResetView(FormView):
    template_name = "password_reset.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("sending_mail:mailing_list")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_object_or_404(CustomUser, email=email)

        token = secrets.token_hex(16)  # 16 - шкала чисел
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/password_reset/{token}/"
        send_mail(
            subject="Восстановление пароля на сайте",
            message=f"Для завершения восстановления пароля перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        messages.success(self.request, "Письмо для восстановления пароля было отправлено на ваш электронный адрес.")

        return super().form_valid(form)


def password_confirm(request, token):
    user = get_object_or_404(CustomUser, token=token)

    if request.method == "POST":
        form = CustomPasswordSetForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("users:login"))
    else:
        form = CustomPasswordSetForm(user)

    template_name = "password_reset_confirm.html"
    return render(request, template_name, {"form": form})
