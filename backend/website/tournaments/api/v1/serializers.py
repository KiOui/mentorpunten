from rest_framework import serializers

from tournaments import models
from transactions.api.v1.serializers import AccountSerializer
from users.api.v1.serializers import UserSerializer


class TournamentSerializer(serializers.ModelSerializer):
    """Tournament Serializer."""

    class Meta:
        """Meta class."""

        model = models.Tournament
        fields = ("id", "name", "slug", "active_from", "active_until")


class TeamSerializer(serializers.ModelSerializer):
    """Team serializer."""

    account = AccountSerializer(many=False)
    members = UserSerializer(many=True)
    tournament = TournamentSerializer(many=False)

    class Meta:
        """Meta class."""

        model = models.Team
        fields = ("id", "name", "tournament", "account", "members")
