import os
import uuid
from datetime import datetime
from pathlib import Path

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from transactions.models import Account

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
    return os.path.join(os.path.join(instance.challenge.folder, "challenge"), main_image_name)


def submission_upload_image_to(instance, filename):
    """Upload submission images to."""
    return os.path.join(os.path.join(instance.challenge.folder, "submissions"), get_random_filename(filename))


class Challenge(models.Model):
    """Challenge."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=challenge_upload_image_to, blank=True, null=True)
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


class Team(models.Model):
    """Team of Users that can hand in Submissions for Challenges."""

    name = models.CharField(max_length=100)
    account = models.OneToOneField(
        Account, on_delete=models.PROTECT, related_name="team"
    )

    @property
    def points(self):
        """Get points of team."""
        return self.account.balance

    def __str__(self):
        """Convert this object to string."""
        return f"{self.name}"


class Submission(models.Model):
    """Submission for a Challenge."""

    challenge = models.ForeignKey(
        Challenge, on_delete=models.PROTECT, related_name="submissions"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=submission_upload_image_to)
    accepted = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        """Convert this object to string."""
        return f"Submission for {self.challenge} for {self.team} at {self.created}"


class ChallengeUser(models.Model):
    """User that can be in a Team."""

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="challenge_user"
    )
    team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.SET_NULL, related_name="members"
    )

    def __str__(self):
        """Convert this object to string."""
        return self.user.__str__()
