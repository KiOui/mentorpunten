from rest_framework import serializers

from tournaments import models
from transactions.api.v1.serializers import AccountSerializer
from users.api.v1.serializers import UserSerializer


class TournamentSerializer(serializers.ModelSerializer):
    """Tournament Serializer."""

    class Meta:
        """Meta class."""

        model = models.Tournament
        fields = ("id", "name", "slug", "active_from", "active_until", "store")


class ItemSerializer(serializers.ModelSerializer):
    """Item Serializer."""

    class Meta:
        """Meta class."""

        model = models.Item
        fields = (
            "id",
            "name",
            "price",
            "item",
            "transaction",
            "created_at",
            "property_of",
            "used",
            "used_at",
        )
        read_only_fields = (
            "id",
            "name",
            "price",
            "transaction",
            "created_at",
            "used_at",
        )


class TeamSerializer(serializers.ModelSerializer):
    """Team serializer."""

    points_account = AccountSerializer(many=False)
    coins_account = AccountSerializer(many=False)
    members = UserSerializer(many=True)
    tournament = TournamentSerializer(many=False)
    items = ItemSerializer(many=True)

    class Meta:
        """Meta class."""

        model = models.Team
        fields = (
            "id",
            "name",
            "tournament",
            "points_account",
            "coins_account",
            "members",
            "items",
        )
