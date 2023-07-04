from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from .views import (
    IndexView,
    LogoutView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("thalia/", include(("thalia.urls", "thalia"), namespace="thalia")),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path(
        "login/",
        RedirectView.as_view(
            url="/thalia/login/" if not settings.DEBUG else "/admin-login",
            query_string=True,
        ),
        name="login",
    ),
    path(
        "admin/login/",
        RedirectView.as_view(url="/login", query_string=True),
        name="login-redirect",
    ),
    path(
        "admin/logout/",
        RedirectView.as_view(url="/logout", query_string=True),
        name="logout-redirect",
    ),
    path("admin-login/", admin.site.login, name="admin-login"),
    path("admin-logout/", admin.site.logout, name="admin-logout"),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
