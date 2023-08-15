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

        cls.normal_user_points_account = Account.objects.create(
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

        cls.normal_user_team = Team.objects.create(
            name="Normal user Team",
            tournament=cls.test_tournament,
            points_account=cls.normal_user_points_account
        )

        cls.normal_user_team.members.add(cls.normal_user)

        cls.challenge = models.Challenge.objects.create(
            name="Test Challenge",
            tournament=cls.test_tournament,
            slug="test-challenge",
            description="This is a test challenge",
            points=5,
        )

        cls.challenge_show_when_submitted = models.Challenge.objects.create(
            name="Test Challenge only show when submitted",
            tournament=cls.test_tournament,
            slug="test-challenge-only-show-when-submitted",
            description="This is a test challenge",
            points=5,
            submission_visibility=models.Challenge.SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION
        )

        cls.test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else",
            file_type="undefined",
            created_by=User.objects.get(pk=1)
        )

        cls.test_file_2 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 2",
            file_type="undefined",
            created_by=User.objects.get(pk=1)
        )

        cls.test_file_3 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 3",
            file_type="undefined",
            created_by=User.objects.get(pk=1)
        )

        cls.test_file_4 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 4",
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
        response = self.client.get(
            reverse("v1:challenge_list"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data), models.Challenge.objects.filter(disabled=False).count())

    def test_retrieve_challenge(self):
        response = self.client.get(
            reverse("v1:challenge_retrieve", kwargs={'pk': self.challenge.pk}),
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_challenge_disabled(self):
        challenge_disabled = models.Challenge.objects.create(
            name="Test Challenge disabled",
            tournament=self.test_tournament,
            slug="test-challenge-disabled",
            description="This is a disabled test challenge",
            points=5,
            disabled=True
        )
        response = self.client.get(
            reverse("v1:challenge_retrieve", kwargs={'pk': challenge_disabled.pk}),
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_list_submissions_not_logged_in(self):
        """Test that non logged in users can not see submissions."""
        models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file_2,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_list_submissions_always_show(self):
        """Test that logged in users can see submissions that are shown on accept."""
        self.client.login(username=self.normal_user.username, password="password")
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        submission_2 = models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file_2,
            accepted=True,
        )


