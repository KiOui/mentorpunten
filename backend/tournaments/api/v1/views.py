from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from tournaments import models
from tournaments.api.v1 import serializers


class TournamentListAPIView(ListAPIView):
    """Tournament List API View."""

    serializer_class = serializers.TournamentSerializer
    queryset = models.Tournament.objects.active_tournaments()

    filter_backends = [filters.SearchFilter]
    search_fields = ("name", "slug",)


class TournamentRetrieveAPIView(RetrieveAPIView):
    """Tournament Retrieve API View."""

    serializer_class = serializers.TournamentSerializer
    queryset = models.Tournament.objects.active_tournaments()


class TeamListAPIView(ListAPIView):
    """Team List API View."""

    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.active_teams()

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ("tournament", "members",)
    search_fields = ("name",)


class TeamRetrieveAPIView(RetrieveAPIView):
    """Team Retrieve API View."""

    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.active_teams()
