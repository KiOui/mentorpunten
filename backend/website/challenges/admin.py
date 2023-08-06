from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin, messages
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from challenges.models import Challenge, Submission


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Challenge Admin."""

    list_display = ("name", "tournament", "active_from", "active_until", "points", "number_of_submissions", "active")
    search_fields = ("name",)
    ordering = (
        "-active_from",
        "-active_until",
        "name",
    )
    list_filter = (
        "tournament",
        ("active_from", DateRangeFilter,),
        ("active_until", DateRangeFilter,),
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

    list_display = ("team", "challenge", "tournament", "created", "updated", "accepted",)
    fields = ('challenge', 'tournament', 'team', 'created', 'updated', 'image', 'image_tag', 'accepted', 'transaction')
    readonly_fields = ('image_tag', 'created', 'updated', 'transaction')

    ordering = (
        "-created",
    )
    list_filter = (
        ("team", AutocompleteListFilter),
        ("challenge", AutocompleteListFilter),
        ("tournament", AutocompleteListFilter),
        "accepted"
    )

    def image_tag(self, obj):
        """Print image in changeform view."""
        return format_html('<img src="{}" width="400px" style="max-width: 100%;" />'.format(obj.image.url))

    image_tag.short_description = 'Image preview'

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """Display warning for already accepted submissions."""
        if object_id:
            obj = self.get_object(request, object_id)
            if (
                Submission.objects.filter(challenge=obj.challenge, team=obj.team, accepted=True)
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