import json
import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from challenges import models
from files.models import File
from tournaments.models import Team, Tournament
from transactions.models import Account

User = get_user_model()
logging.disable()


class OrderAPITests(APITestCase):
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
        cls.normal_user = User.objects.get(pk=2)

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

    def test_list_challenges(self):
        models.Challenge.objects.create(
            name="Test Challenge disabled",
            tournament=self.test_tournament,
            slug="test-challenge-disabled",
            description="This is a disabled test challenge",
            points=5,
        )
        self.client.login(username=self.normal_user.username, password="password")
        response = self.client.get(
            reverse("v1:challenge_list"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data), models.Challenge.objects.filter(disabled=False).count())

