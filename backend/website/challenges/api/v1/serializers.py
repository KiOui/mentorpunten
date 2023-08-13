from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from challenges import models
from challenges.models import Submission
from files.api.v1.serializers import FileSerializer
from mentorpunten.api.serializers import WritableModelSerializer
from tournaments.api.v1.serializers import TeamSerializer, TournamentSerializer
from transactions.api.v1.serializers import TransactionSerializer
from users.api.v1.serializers import UserSerializer
from drf_spectacular.utils import extend_schema_field


class SubmissionsWithoutChallengeSerializer(serializers.ModelSerializer):
    """Submission Serializer without Challenge field."""

    team = TeamSerializer(many=False)
    transaction = TransactionSerializer(many=False, read_only=True)
    file = FileSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = models.Submission
        fields = [
            "team",
            "created",
            "updated",
            "file",
            "accepted",
            "transaction",
        ]
        read_only_fields = ["created", "updated", "transaction"]


class ChallengeSerializer(serializers.ModelSerializer):
    """Challenge serializer."""

    completed = SerializerMethodField()
    tournament = TournamentSerializer(many=False, read_only=True)

    @extend_schema_field(serializers.BooleanField)
    def get_completed(self, instance):
        """Get completed value of serializer."""
        request = self.context.get("request", None)
        if (
            request is not None
            and request.user is not None
            and request.user.is_authenticated
        ):
            return Submission.objects.filter(
                team__members__in=[request.user], challenge=instance, accepted=True
            ).exists()
        else:
            return None

    class Meta:
        """Meta class."""

        model = models.Challenge
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "tournament",
            "disabled",
            "active_from",
            "active_until",
            "points",
            "completed",
            "submission_visibility",
        ]
        read_only_fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "tournament",
            "disabled",
            "active_from",
            "active_until",
            "points",
            "completed",
            "submission_visibility",
        ]


class SubmissionSerializer(WritableModelSerializer):
    """Submission serializer."""

    challenge = ChallengeSerializer(many=False)
    team = TeamSerializer(many=False)
    points_transaction = TransactionSerializer(many=False, read_only=True)
    coins_transaction = TransactionSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False)
    updated_by = UserSerializer(many=False)
    file = FileSerializer(many=False)

    class Meta:
        """Meta class."""

        model = models.Submission
        fields = [
            "id",
            "challenge",
            "team",
            "tournament",
            "created",
            "created_by",
            "updated",
            "updated_by",
            "file",
            "accepted",
            "points_transaction",
            "coins_transaction",
        ]
        read_only_fields = [
            "id",
            "created",
            "updated",
            "points_transaction",
            "coins_transaction",
        ]
