from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rangefilter.filters import DateRangeFilter

from .models import Tournament, Team

User = get_user_model()


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):

    list_display = ['name', 'active_from', 'active_until']
    search_fields = ('name',)
    list_filter = (
        ("active_from", DateRangeFilter,),
        ("active_until", DateRangeFilter,),
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

        if self.instance:
            teams = Team.objects.filter(members__in=members).exclude(id=self.instance.id)
        else:
            teams = Team.objects.filter(members__in=members)

        if teams.count() > 0:
            # Some of the team members are in other teams.
            error_message = []
            for member in members:
                if self.instance:
                    member_team = Team.objects.filter(members__in=[member]).exclude(id=self.instance.id)
                else:
                    member_team = Team.objects.filter(members__in=[member])

                if member_team.count() > 0:
                    error_message.append(f"'{member} is also a member of team(s): {', '.join([team.name for team in member_team])}'")
            raise ValidationError(f"The following members are also members of other teams: {', '.join(error_message)}")
        return members

    class Meta:
        """Meta class."""

        model = Team
        exclude = []


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    def balance(self, instance: Team):
        """Get balance."""
        return instance.account.balance

    def member_count(self, instance: Team):
        """Get member count."""
        return instance.members.count()

    list_display = ['name', 'tournament', 'balance', 'member_count']
    search_fields = ('name',)
    list_filter = ('tournament',)
    form = TeamAdminForm
