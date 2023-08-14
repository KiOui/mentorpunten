from django.db import models


class Item(models.Model):
    """Item model."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        """Convert this object to string."""
        return self.name


class Store(models.Model):
    """Store model."""

    name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(Item)

    def __str__(self):
        """Convert this object to string."""
        return self.name
