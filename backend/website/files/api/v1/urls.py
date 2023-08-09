from django.urls import path
from files.api.v1.views import (
    FileDirectUploadStartApi,
    FileDirectUploadFinishApi,
    FileDirectUploadLocalApi,
)

app_name = "files"

urlpatterns = [
    path(
        "upload/start/",
        FileDirectUploadStartApi.as_view(),
        name="files_upload_start",
    ),
    path(
        "upload/finish/",
        FileDirectUploadFinishApi.as_view(),
        name="files_upload_finish",
    ),
    path(
        "upload/local/<str:file_id>/",
        FileDirectUploadLocalApi.as_view(),
        name="files_upload_local",
    )
]
