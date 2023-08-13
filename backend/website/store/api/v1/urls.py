from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreListAPIView.as_view(), name="store_list"),
    path(
        "<int:pk>/",
        views.StoreRetrieveAPIView.as_view(),
        name="store_retrieve",
    ),
]
