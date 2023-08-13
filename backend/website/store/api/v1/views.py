from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView

from store import models
from store.api.v1 import serializers


class StoreListAPIView(ListAPIView):
    """Store List API View."""

    serializer_class = serializers.StoreSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)

    def get_queryset(self):
        """Get the queryset."""
        return models.Store.objects.all()


class StoreRetrieveAPIView(RetrieveAPIView):
    """Store Retrieve API View."""

    serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        """Get the queryset."""
        return models.Tournament.objects.all()
