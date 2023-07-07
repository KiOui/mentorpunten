from rest_framework import serializers

from transactions import models


class AccountSerializer(serializers.ModelSerializer):
    """Account Serializer."""

    class Meta:
        """Meta class."""

        model = models.Account
        fields = ["created_at", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction Serializer."""

    class Meta:
        """Meta class."""

        model = models.Transaction
        fields = ["id", "account", "amount", "timestamp", "description", "processor", "balance_after"]
