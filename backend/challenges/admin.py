from django.contrib import admin
from django.contrib.admin import TabularInline

from challenges.models import Challenge, Team, Submission, ChallengeUser


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


@admin.register(ChallengeUser)
class ChallengeUserAdmin(admin.ModelAdmin):
    """Challenge User Inline."""

    list_display = ("user", "team")
    search_fields = ("user",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Team Admin."""

    list_display = ("name", "points",)
    search_fields = ("name",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Submission Admin."""

    list_display = ("team", "challenge", "created", "updated", "accepted",)
