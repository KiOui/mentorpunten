from django.urls import path
from . import views

urlpatterns = [
    path("", views.TournamentListAPIView.as_view(), name="tournament_list"),
    path(
        "<int:pk>/",
        views.TournamentRetrieveAPIView.as_view(),
        name="tournament_retrieve",
    ),
    path("teams/", views.TeamListAPIView.as_view(), name="team_list"),
    path("teams/<int:pk>/", views.TeamRetrieveAPIView.as_view(), name="team_retrieve"),
    path("items/", views.ItemCreateAPIView.as_view(), name="item_create"),
]
