from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin, messages
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from challenges.models import Challenge, Submission


@admin.register(Challenge)
class ChallengeAdmin(ImportExportModelAdmin):
    """Challenge Admin."""

    list_display = (
        "name",
        "tournament",
        "active_from",
        "active_until",
        "points",
        "number_of_submissions",
        "active",
    )
    search_fields = ("name",)
    ordering = (
        "-active_from",
        "-active_until",
        "name",
    )
    list_filter = (
        "tournament",
        (
            "active_from",
            DateRangeFilter,
        ),
        (
            "active_until",
            DateRangeFilter,
        ),
    )
    prepopulated_fields = {"slug": ("name",)}

    def number_of_submissions(self, obj: Challenge):
        """Get the number of submissions."""
        return Submission.objects.filter(challenge=obj).count()

    def active(self, obj: Challenge):
        """Get whether a Challenge is currently active."""
        return obj.active

    active.boolean = True


@admin.register(Submission)
class SubmissionAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    """Submission Admin."""

    list_display = (
        "team",
        "challenge",
        "tournament",
        "created",
        "updated",
        "accepted",
        "type",
    )
    fields = (
        "challenge",
        "tournament",
        "team",
        "created",
        "updated",
        "file_tag",
        "accepted",
        "points_transaction",
        "coins_transaction",
    )
    readonly_fields = (
        "file_tag",
        "created",
        "updated",
        "points_transaction",
        "coins_transaction",
    )

    ordering = ("-created",)
    list_filter = (
        ("team", AutocompleteListFilter),
        ("challenge", AutocompleteListFilter),
        ("tournament", AutocompleteListFilter),
        "accepted",
    )

    def type(self, obj: Submission):
        """Get file type."""
        if obj.file.is_photo:
            return "Photo"
        elif obj.file.is_video:
            return "Video"
        else:
            return "Other"

    def file_tag(self, obj: Submission):
        """Print image in changeform view."""
        if obj.file.is_photo:
            return format_html(
                '<img src="{}" width="400px" style="max-width: 100%;" />'.format(
                    obj.file.compressed_file.url
                    if obj.file.compressed_file.name
                    else obj.file.file.url
                )
            )
        elif obj.file.is_video:
            return format_html(
                '<video controls style="max-width: 100%; max-height: 600px;"> \
                    <source src="{}"/> \
                    Your browser does not support the video tag. \
                </video>'.format(
                    obj.file.compressed_url.url
                    if obj.file.compressed_file.name
                    else obj.file.file.url
                )
            )
        else:
            return "No format available for this file."

    file_tag.short_description = "Preview"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """Display warning for already accepted submissions."""
        if object_id:
            obj = self.get_object(request, object_id)
            if (
                Submission.objects.filter(
                    challenge=obj.challenge, team=obj.team, accepted=True
                )
                .exclude(pk=obj.pk)
                .exists()
            ):
                self.message_user(
                    request,
                    "This team already has an accepted Submission for this Challenge.",
                    level=messages.WARNING,
                )
        return super().changeform_view(request, object_id, form_url, extra_context)

    class Media:
        """Necessary to use AutocompleteFilter."""
