from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from .views import (
    IndexView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("thalia/", include(("thalia.urls", "thalia"), namespace="thalia")),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
