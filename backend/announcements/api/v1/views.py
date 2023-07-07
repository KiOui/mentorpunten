from rest_framework.generics import ListAPIView

from announcements.api.v1.serializers import AnnouncementSerializer
from announcements.models import Announcement


class AnnouncementListAPIView(ListAPIView):
    """Announcement List API View."""

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.visible()
