from django.urls import path

from .views import MeRetrieveAPIView

app_name = "users_api"

urlpatterns = [
    path("me/", MeRetrieveAPIView.as_view(), name="me"),
]
