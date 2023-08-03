import os
import uuid
from datetime import datetime
from pathlib import Path

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from mentorpunten.services import convert_image
from tournaments.models import Tournament, Team
from transactions.models import Account, Transaction

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
    return os.path.join(os.path.join(instance.challenge.folder, "challenge"), main_image_name)


def submission_upload_image_to(instance, filename):
    """Upload submission images to."""
    return os.path.join(os.path.join(instance.challenge.folder, "submissions"), get_random_filename(filename))


class Challenge(models.Model):
    """Challenge."""

    name = models.CharField(max_length=80, unique=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
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


class Submission(models.Model):
    """Submission for a Challenge."""

    challenge = models.ForeignKey(
        Challenge, on_delete=models.PROTECT, related_name="submissions"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="submissions_created_by")
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="submissions_updated_by")
    image = models.ImageField(verbose_name=_("image"), upload_to=submission_upload_image_to)
    thumbnail = models.ImageField(verbose_name=_("thumbnail"), upload_to=submission_upload_image_to)
    image_webp = models.ImageField(verbose_name=_("image webp"), upload_to=submission_upload_image_to)
    accepted = models.BooleanField(null=True, blank=True, default=None)
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.SET_NULL)

    def __init__(self, *args, **kwargs):
        """Set old image variable."""
        super(Submission, self).__init__(*args, **kwargs)
        if kwargs.get("image", None) is not None:
            self._image = None
        else:
            self._image = self.image

    def save(self, *args, **kwargs):
        """Convert images to webp on save."""
        if self.image != self._image:
            # Image has been updated
            self.image = convert_image(self.image, "jpeg", to_name=get_random_filename(self.image.name))
            self.thumbnail = convert_image(
                self.image, "jpeg", resize_to=(600, 600), to_name="thumb_" + Path(self.image.name).stem + ".jpeg"
            )
            self.image_webp = convert_image(self.image, "webp")
        super().save(*args, **kwargs)

    def __str__(self):
        """Convert this object to string."""
        return f"Submission for {self.challenge} for {self.team} at {self.created}"
