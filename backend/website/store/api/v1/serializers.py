from rest_framework import serializers

from store import models


class ItemSerializer(serializers.ModelSerializer):
    """Item Serializer."""

    class Meta:
        """Meta class."""

        model = models.Item
        fields = ("id", "name", "description", "price")


class StoreSerializer(serializers.ModelSerializer):
    """Store Serializer."""

    items = ItemSerializer(many=True)

    class Meta:
        """Meta class."""

        model = models.Store
        fields = ("id", "name", "items")
