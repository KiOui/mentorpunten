from django.apps import AppConfig


class ChallengesConfig(AppConfig):
    """Challenges Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "challenges"

    def ready(self):
        """Register signals."""
        import challenges.signals  # noqa
