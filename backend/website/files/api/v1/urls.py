from django.conf import settings
from django.urls import path
from files.api.v1.views import (
    TemporaryFileUploadListCreateAPIView,
    TemporaryFileUploadRetrieveUpdateDestroyAPIView,
    FileListCreateAPIView,
    DebugDirectFileUploadView,
)

app_name = "files"

urlpatterns = [
    path(
        "",
        FileListCreateAPIView.as_view(),
        name="file_listcreate",
    ),
    path(
        "temporary/",
        TemporaryFileUploadListCreateAPIView.as_view(),
        name="temporary_file_upload_listcreate",
    ),
    path(
        "temporary/<str:pk>/",
        TemporaryFileUploadRetrieveUpdateDestroyAPIView.as_view(),
        name="temporary_file_upload_retrieveupdatedestroy",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "direct/",
            DebugDirectFileUploadView.as_view(),
            name="debug_direct_file_upload",
        )
    ]
