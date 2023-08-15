import base64
import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from challenges import models
from files.models import File
from tournaments.models import Tournament, Team
from transactions.models import Account

User = get_user_model()
logging.disable()


class ChallengsSignalsTests(TestCase):
    """Challenges Signals Tests."""

    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_tournament = Tournament.objects.create(
            name="Test Tournament",
            slug="test-tournament",
            active_from=timezone.now(),
            active_until=timezone.now() + timedelta(days=7),
        )

        cls.points_account = Account.objects.create(
            name="Test Team (Points Account)"
        )

        cls.test_user = User.objects.get(pk=1)

        cls.test_team = Team.objects.create(
            name="Test Team",
            tournament=cls.test_tournament,
            points_account=cls.points_account
        )

        cls.test_team.members.add(cls.test_user)

        cls.challenge = models.Challenge.objects.create(
            name="Test Challenge",
            tournament=cls.test_tournament,
            slug="test-challenge",
            description="This is a test challenge",
            points=5,
        )

        cls.test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else",
            file_type="undefined",
            created_by=User.objects.get(pk=1)
        )

    def test_add_points_on_submission_accept(self):
        self.assertEquals(self.test_team.points_account.balance, 0)

        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=False,
        )

        self.assertEquals(self.test_team.points_account.balance, 0)
        submission.accepted = True
        submission.save()
        self.assertEquals(self.test_team.points_account.balance, 5)

    def test_add_coins_on_submission_accept(self):
        self.test_team.coins_account = Account.objects.create(
            name="Test team (coins account)",
        )

        self.assertEquals(self.test_team.coins_account.balance, 0)
        self.assertEquals(self.test_team.points_account.balance, 0)

        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=False,
        )

        self.assertEquals(self.test_team.coins_account.balance, 0)
        self.assertEquals(self.test_team.points_account.balance, 0)
        submission.accepted = True
        submission.save()
        self.assertEquals(self.test_team.coins_account.balance, 5)
        self.assertEquals(self.test_team.points_account.balance, 5)

