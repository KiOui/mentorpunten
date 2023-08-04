from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from queryable_properties.managers import QueryablePropertiesManager

from queryable_properties.properties import RangeCheckProperty

from transactions.models import Account

User = get_user_model()


class TournamentQueryset(models.QuerySet):
    """Tournament queryset."""

    def active(self):
        """Only active Tournaments."""
        current_time = timezone.now()
        return self.filter(active_from__lte=current_time, active_until__gt=current_time)

    def revealed(self):
        """Only revealed Tournaments."""
        current_time = timezone.now()
        return self.filter(active_from__lte=current_time)


class TournamentManager(QueryablePropertiesManager):
    """Custom manager for Tournaments."""

    def get_queryset(self):
        """Get product Queryset."""
        return TournamentQueryset(self.model, using=self._db)

    def active_tournaments(self):
        """Only active Tournaments."""
        return self.get_queryset().active()

    def revealed_tournaments(self):
        """Only revealed Tournaments."""
        return self.get_queryset().revealed()


class Tournament(models.Model):
    """Tournament class."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    active_from = models.DateTimeField()
    active_until = models.DateTimeField()
    active = RangeCheckProperty("active_from", "active_until", timezone.now)

    objects = TournamentManager()

    def __str__(self):
        """Convert this object to string."""
        return f"{self.name}"

    class Meta:
        """Meta class."""

        ordering = ("name",)


class TeamQueryset(models.QuerySet):
    """Team queryset."""

    def active(self):
        """Only active Teams."""
        current = timezone.now()
        return self.filter(tournament__active_from__lte=current, tournament__active_until__gt=current)


class TeamManager(QueryablePropertiesManager):
    """Custom manager for Teams."""

    def get_queryset(self):
        """Get product Queryset."""
        return TeamQueryset(self.model, using=self._db)

    def active_teams(self):
        """Only active Teams."""
        return self.get_queryset().active()


class Team(models.Model):
    """Team of Users that can hand in Submissions for Challenges."""

    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    members = models.ManyToManyField(User)
    account = models.OneToOneField(
        Account, on_delete=models.PROTECT, related_name="team", unique=True
    )

    objects = TeamManager()

    @property
    def points(self):
        """Get points of team."""
        return self.account.balance

    def __str__(self):
        """Convert this object to string."""
        return f"{self.name}"

    class Meta:
        """Meta class."""

        ordering = ("name",)
        unique_together = ("name", "tournament",)
