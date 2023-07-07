from django.contrib import admin

from challenges.models import Challenge


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Challenge Admin."""

    list_display = ("name", "active_from", "active_until", "points", "active")
    search_fields = ("name",)
    ordering = (
        "-active_from",
        "-active_until",
        "name",
    )
    prepopulated_fields = {"slug": ("name",)}

    def active(self, obj: Challenge):
        """Get whether a Challenge is currently active."""
        return obj.active

    active.boolean = True
