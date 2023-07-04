from django.urls import path
from .views import LoginView, CallbackView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("callback/", CallbackView.as_view(), name="callback"),
]
