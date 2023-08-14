from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from .models import Tournament, Team, Item
from .resources import TeamResource

User = get_user_model()


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Tournament Admin."""

    list_display = ["name", "active_from", "active_until"]
    search_fields = ("name",)
    list_filter = (
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


class TeamAdminForm(forms.ModelForm):
    """Team Admin Form."""

    members = forms.ModelMultipleChoiceField(
        User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("members", False),
    )

    def clean_members(self):
        """Clean members."""
        members = self.cleaned_data.get("members")
        tournament = self.cleaned_data.get("tournament")

        if self.instance:
            teams = Team.objects.filter(
                members__in=members, tournament=tournament
            ).exclude(id=self.instance.id)
        else:
            teams = Team.objects.filter(members__in=members, tournament=tournament)

        if teams.count() > 0:
            # Some of the team members are in other teams.
            error_message = []
            for member in members:
                if self.instance:
                    member_team = Team.objects.filter(
                        members__in=[member], tournament=tournament
                    ).exclude(id=self.instance.id)
                else:
                    member_team = Team.objects.filter(
                        members__in=[member], tournament=tournament
                    )

                if member_team.count() > 0:
                    error_message.append(
                        f"'{member} is also a member of team(s): {', '.join([team.name for team in member_team])}'"
                    )
            raise ValidationError(
                f"The following members are also members of other teams: {', '.join(error_message)}"
            )
        return members

    class Meta:
        """Meta class."""

        model = Team
        exclude = []


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin."""

    list_display = ["name", "price", "item", "property_of", "used"]
    search_fields = ("name",)
    list_filter = (
        "property_of",
        "item",
        "used",
    )


class ItemInline(admin.TabularInline):
    """Inline of items."""

    model = Item
    fields = (
        "name",
        "price",
        "item",
        "transaction",
        "created_at",
        "used",
        "used_at",
    )
    readonly_fields = (
        "transaction",
        "created_at",
        "used_at",
    )
    extra = 0
    ordering = ("created_at",)


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    """Team Admin."""

    def balance(self, instance: Team):
        """Get balance."""
        return instance.points_account.balance

    def member_count(self, instance: Team):
        """Get member count."""
        return instance.members.count()

    list_display = ["name", "tournament", "balance", "member_count"]
    search_fields = ("name",)
    list_filter = ("tournament",)
    form = TeamAdminForm
    resource_class = TeamResource

    inlines = [ItemInline]
