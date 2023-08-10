from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from files.models import File, TemporaryFileUpload


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """File Admin."""

    list_display = (
        "file_name",
        "original_file_name",
        "file_type",
        "created_at",
    )

    search_fields = (
        "file_name",
        "original_file_name",
    )

    ordering = (
        "-created_at",
        "file_name",
    )

    list_filter = (
        (
            "created_at",
            DateRangeFilter,
        ),
        "file_type",
    )


@admin.register(TemporaryFileUpload)
class TemporaryFileUploadAdmin(admin.ModelAdmin):
    """Temporary File Upload Admin."""

    list_display = ("file_name",)
