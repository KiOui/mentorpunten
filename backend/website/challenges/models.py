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
from mentorpunten.services import convert_image
from tournaments.models import Tournament, Team
from transactions.models import Transaction

from django.utils.translation import gettext_lazy as _

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


def submission_upload_image_to(instance, filename):
    """Upload submission images to."""
    return os.path.join(
        os.path.join(instance.challenge.folder, "submissions"),
        get_random_filename(filename),
    )


def submission_upload_video_to(instance, filename):
    """Upload submission videos to."""
    return os.path.join(
        os.path.join(instance.challenge.folder, "submissions_videos"),
        get_random_filename(filename),
    )


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
    file = models.OneToOneField(File, on_delete=models.PROTECT, related_name="submission")
    accepted = models.BooleanField(null=True, blank=True, default=None)
    transaction = models.ForeignKey(
        Transaction, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        """Convert this object to string."""
        return f"Submission for {self.challenge} for {self.team} at {self.created}"

    class Meta:
        """Meta class."""

        ordering = ("-created",)
