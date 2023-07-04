from django.db import models


class Challenge(models.Model):
    """Challenge."""

    name = models.CharField(max_length=200)
    points = models.PositiveIntegerField()