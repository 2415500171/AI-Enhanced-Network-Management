from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView
from .views import signup_view

app_name = "users"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="users:login", permanent=False)),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
]