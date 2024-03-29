import os
import uuid
from datetime import datetime
from pathlib import Path

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils import timezone
from queryable_properties.managers import QueryablePropertiesManager

from files.models import File
from tournaments.models import Tournament, Team
from transactions.models import Transaction

User = get_user_model()


def get_random_filename(current_filename):
    """Get a random filename by overwriting the filename with a random string."""
    extension = Path(current_filename).suffix
    unique_id = uuid.uuid4()
    return f"{unique_id}{extension}"


def challenge_upload_image_to(instance, filename):
    """Upload challenge image to."""
    extension = Path(filename).suffix
    main_image_name = f"main-image{extension}"
    return os.path.join(os.path.join(instance.folder, "challenge"), main_image_name)


class ChallengeQueryset(models.QuerySet):
    """Challenge queryset."""

    def active(self):
        """Only active Challenges."""
        current_time = timezone.now()
        return self.filter(
            Q(disabled=False)
            & (Q(active_from=None) | Q(active_from__lte=current_time))
            & (Q(active_until=None) | Q(active_until__gt=current_time))
        )

    def revealed(self):
        """Only revealed Challenges."""
        current_time = timezone.now()
        return self.filter(
            Q(disabled=False) & (Q(active_from=None) | Q(active_from__lte=current_time))
        )


class ChallengeManager(QueryablePropertiesManager):
    """Custom manager for Challenges."""

    def get_queryset(self):
        """Get Challenge Queryset."""
        return ChallengeQueryset(self.model, using=self._db)

    def active_challenges(self):
        """Only active Challenges."""
        return self.get_queryset().active()

    def revealed_challenges(self):
        """Only revealed Challenges."""
        return self.get_queryset().revealed()


class Challenge(models.Model):
    """Challenge."""

    SUBMISSIONS_ALWAYS_VISIBLE = 1
    SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION = 2

    SUBMISSION_VISIBILITY_CHOICES = [
        (SUBMISSIONS_ALWAYS_VISIBLE, "Submissions are always visible"),
        (
            SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION,
            "Submissions are visible when a team posted an accepted submission in the challenge",
        ),
    ]

    name = models.CharField(max_length=80, unique=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to=challenge_upload_image_to, blank=True, null=True
    )
    disabled = models.BooleanField(default=False)
    active_from = models.DateTimeField(
        help_text="From which point in time this challenge will be active. Leave empty for no start time.",
        null=True,
        blank=True,
    )
    active_until = models.DateTimeField(
        help_text="Until which point in time this challenge will be active. Leave empty for no end time.",
        null=True,
        blank=True,
    )
    points = models.PositiveIntegerField()
    submission_visibility = models.PositiveIntegerField(
        choices=SUBMISSION_VISIBILITY_CHOICES, default=SUBMISSIONS_ALWAYS_VISIBLE
    )

    objects = ChallengeManager()

    @property
    def folder(self):
        """Get folder."""
        return f"challenges/{self.slug}/"

    @property
    def active(self):
        """Get whether a Challenge is currently active."""
        if self.disabled:
            return False

        timezone = pytz.timezone(settings.TIME_ZONE)
        current_time = timezone.localize(datetime.now())

        if self.active_from is not None and self.active_from > current_time:
            return False
        elif self.active_until is not None and self.active_until < current_time:
            return False
        else:
            return True

    @property
    def revealed(self):
        """Get whether a Challenge has been revealed."""
        if self.disabled:
            return False

        if not self.tournament.revealed:
            return False

        timezone = pytz.timezone(settings.TIME_ZONE)
        current_time = timezone.localize(datetime.now())

        return self.active_from is None or self.active_from <= current_time

    def __str__(self):
        """Convert this object to string."""
        return self.name


class Submission(models.Model):
    """Submission for a Challenge."""

    challenge = models.ForeignKey(
        Challenge, on_delete=models.PROTECT, related_name="submissions"
    )
    tournament = models.ForeignKey(
        Tournament,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submissions",
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="submissions_created_by",
    )
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="submissions_updated_by",
    )
    file = models.OneToOneField(
        File, on_delete=models.PROTECT, related_name="submission"
    )
    accepted = models.BooleanField(null=True, blank=True, default=None)
    points_transaction = models.ForeignKey(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="points_submission",
    )
    coins_transaction = models.ForeignKey(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="coins_submission",
    )

    def create_points_transaction(instance):
        """Create a points transaction for this submission."""
        if instance.points_transaction is None:
            instance.points_transaction = Transaction.objects.create(
                account=instance.team.points_account,
                amount=instance.challenge.points,
                description=f"Completed challenge {instance.challenge.name}",
            )

    def create_coins_transaction(instance):
        """Create a coins transaction for this submission."""
        if (
            instance.coins_transaction is None
            and instance.team.coins_account is not None
        ):
            instance.coins_transaction = Transaction.objects.create(
                account=instance.team.coins_account,
                amount=instance.challenge.points,
                description=f"Completed challenge {instance.challenge.name}",
            )

    def __str__(self):
        """Convert this object to string."""
        return f"Submission for {self.challenge} for {self.team} at {self.created}"

    class Meta:
        """Meta class."""

        ordering = ("-created",)
