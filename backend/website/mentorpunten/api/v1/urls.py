from django.urls import path, include
from rest_framework.schemas import get_schema_view

from mentorpunten.api.openapi import OpenAPISchemaGenerator

app_name = "v1"

urlpatterns = [
    path("announcements/", include("announcements.api.v1.urls")),
    path("challenges/", include("challenges.api.v1.urls")),
    path("stores/", include("store.api.v1.urls")),
    path("tournaments/", include("tournaments.api.v1.urls")),
    path("transactions/", include("transactions.api.v1.urls")),
    path("users/", include("users.api.v1.urls")),
    path("files/", include("files.api.v1.urls", namespace="files")),
    path(
        "schema",
        get_schema_view(
            title="API v1",
            url="/api/v1/",
            version=1,
            urlconf="mentorpunten.api.v1.urls",
            generator_class=OpenAPISchemaGenerator,
        ),
        name="schema-v1",
    ),
]
