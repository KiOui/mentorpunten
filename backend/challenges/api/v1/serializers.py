from rest_framework import serializers

from challenges import models
from mentorpunten.api.serializers import WritableModelSerializer
from transactions.api.v1.serializers import AccountSerializer
from users.api.v1.serializers import UserSerializer


class ChallengeSerializer(serializers.ModelSerializer):
    """Challenge serializer."""

    class Meta:
        """Meta class."""

        model = models.Challenge
        fields = ["name", "slug", "description", "image", "disabled", "active_from", "active_until", "points"]


class TeamSerializer(serializers.ModelSerializer):
    """Team serializer."""

    account = AccountSerializer(many=False)
    members = UserSerializer(many=True)

    class Meta:
        """Meta class."""

        model = models.Team
        fields = ["name", "account", "members"]


class SubmissionSerializer(WritableModelSerializer):
    """Submission serializer."""

    challenge = ChallengeSerializer(many=False, read_only=True)
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = models.Submission
        fields = ["challenge", "team", "created", "updated", "image", "accepted"]
        read_only_fields = ["challenge", "team", "created", "updated", "image"]


class ChallengeUserSerializer(serializers.ModelSerializer):
    """Challenge User Serializer."""

    user = UserSerializer(many=False, read_only=True)
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = models.ChallengeUser
        fields = ["user", "team"]
        read_only_fields = ["user", "team"]
