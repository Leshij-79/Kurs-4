from django.urls import path

from users.apps import UsersConfig

from . import views
from .views import UserLoginView, RegisterView, email_verification, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView, name="logout"),
    path("user/profile/<int:pk>", UserProfileView.as_view(), name="profile"),
    path("email-confurm/<str:token>/", email_verification, name="email-confirm"),
]