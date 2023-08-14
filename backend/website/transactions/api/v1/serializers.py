from rest_framework import serializers

from mentorpunten.api.serializers import WritableModelSerializer
from transactions import models


class AccountSerializer(serializers.ModelSerializer):
    """Account Serializer."""

    class Meta:
        """Meta class."""

        model = models.Account
        fields = ["id", "created_at", "balance"]


class TransactionSerializer(WritableModelSerializer):
    """Transaction Serializer."""

    account = AccountSerializer(many=False, read_only=False)

    class Meta:
        """Meta class."""

        model = models.Transaction
        fields = [
            "id",
            "account",
            "amount",
            "timestamp",
            "description",
            "processor",
            "balance_after",
        ]
        read_only_fields = (
            "id",
            "timestamp",
            "balance_after",
        )
