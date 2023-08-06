from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("thalia/", include(("thalia.urls", "thalia"), namespace="thalia")),
    path("api/", include("mentorpunten.api.urls")),
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
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("admin-login/", admin.site.login, name="admin-login"),
    path("admin-logout/", admin.site.logout, name="admin-logout"),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
