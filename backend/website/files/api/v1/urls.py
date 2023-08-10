from django.urls import path
from files.api.v1.views import (
    FileUploadStartApi,
    FileUploadFinishApi,
    FileCompressedApi,
    FileUploadLocalApi,
)

app_name = "files"

urlpatterns = [
    path(
        "upload/start/",
        FileUploadStartApi.as_view(),
        name="files_upload_start",
    ),
    path(
        "upload/finish/",
        FileUploadFinishApi.as_view(),
        name="files_upload_finish",
    ),
    path(
        "compressed/",
        FileCompressedApi.as_view(),
        name="files_compressed",
    ),
    path(
        "upload/local/<str:file_id>/",
        FileUploadLocalApi.as_view(),
        name="files_upload_local",
    )
]
