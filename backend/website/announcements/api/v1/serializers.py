from rest_framework import serializers

from announcements import models


class AnnouncementSerializer(serializers.ModelSerializer):
    """Announcement serializer."""

    class Meta:
        """Meta class."""

        model = models.Announcement
        fields = ["id", "content", "icon"]
