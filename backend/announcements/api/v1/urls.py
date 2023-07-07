from django.urls import path
from announcements.api.v1.views import AnnouncementListAPIView

app_name = "announcements_api"

urlpatterns = [
    path("", AnnouncementListAPIView.as_view(), name="announcement_list"),
]
