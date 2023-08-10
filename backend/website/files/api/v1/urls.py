from django.urls import path
from files.api.v1.views import (
    TemporaryFileUploadListCreateAPIView,
    TemporaryFileUploadRetrieveUpdateDestroyAPIView,
    FileListCreateAPIView,
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
