from django.urls import path

from website.users.views import LogoutView

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
