from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from challenges.models import ChallengeUser

User = get_user_model()


@receiver(post_save, sender=User)
def create_challenge_user(sender, instance, created, **kwargs):
    """Create a ChallengeUser when a User gets created."""
    if created:
        ChallengeUser.objects.create(user=instance)
