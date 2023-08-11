from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from tournaments import models
from tournaments.api.v1 import serializers


class TournamentListAPIView(ListAPIView):
    """Tournament List API View."""

    serializer_class = serializers.TournamentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = (
        "name",
        "slug",
    )

    def get_queryset(self):
        """Get the queryset."""
        return models.Tournament.objects.all().order_by("active_from")


class TournamentRetrieveAPIView(RetrieveAPIView):
    """Tournament Retrieve API View."""

    serializer_class = serializers.TournamentSerializer

    def get_queryset(self):
        """Get the queryset."""
        return models.Tournament.objects.all()


class TeamListAPIView(ListAPIView):
    """Team List API View."""

    serializer_class = serializers.TeamSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = (
        "tournament",
        "members",
    )
    search_fields = ("name",)

    def get_queryset(self):
        """Get the queryset."""
        return models.Team.objects.all()


class TeamRetrieveAPIView(RetrieveAPIView):
    """Team Retrieve API View."""

    serializer_class = serializers.TeamSerializer

    def get_queryset(self):
        """Get the queryset."""
        return models.Team.objects.all()
