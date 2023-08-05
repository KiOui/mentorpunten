import secrets
import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


def get_random_challenge():
    """Get random challenge."""
    return secrets.token_urlsafe(40)


class AuthenticationRequest(models.Model):
    """Authentication Request for OAuth."""

    state = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    challenge = models.CharField(max_length=80, default=get_random_challenge)

    def __str__(self):
        """Convert this object to string."""
        return f"{self.state}"


class ThaliaUser(models.Model):
    """Thalia User object."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="thalia_user"
    )
    thalia_id = models.BigIntegerField()

    def __str__(self):
        """Convert this object to string."""
        return f"{self.thalia_id}"
