from django.urls import path

from .views import MeRetrieveAPIView, LogoutAPIView

app_name = "users_api"

urlpatterns = [
    path("me/", MeRetrieveAPIView.as_view(), name="me"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
