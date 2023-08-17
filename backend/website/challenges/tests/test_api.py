import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
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

        cls.points_account = Account.objects.create(name="Test Team (Points Account)")

        cls.normal_user_points_account = Account.objects.create(
            name="Test Team (Points Account)"
        )

        cls.test_user = User.objects.get(pk=1)
        cls.normal_user = User.objects.get(pk=2)
        cls.normal_user.set_password("password")
        cls.normal_user.save()

        cls.test_team = Team.objects.create(
            name="Test Team",
            tournament=cls.test_tournament,
            points_account=cls.points_account,
        )

        cls.test_team.members.add(cls.test_user)

        cls.normal_user_team = Team.objects.create(
            name="Normal user Team",
            tournament=cls.test_tournament,
            points_account=cls.normal_user_points_account,
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
            submission_visibility=models.Challenge.SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION,
        )

        cls.test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else",
            file_type="undefined",
            created_by=User.objects.get(pk=1),
        )

        cls.test_file_2 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 2",
            file_type="undefined",
            created_by=User.objects.get(pk=1),
        )

        cls.test_file_3 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 3",
            file_type="undefined",
            created_by=User.objects.get(pk=1),
        )

        cls.test_file_4 = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="something else 4",
            file_type="undefined",
            created_by=User.objects.get(pk=1),
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
        self.assertEquals(
            len(response.data), models.Challenge.objects.filter(disabled=False).count()
        )

    def test_retrieve_challenge(self):
        response = self.client.get(
            reverse("v1:challenge_retrieve", kwargs={"pk": self.challenge.pk}),
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
            disabled=True,
        )
        response = self.client.get(
            reverse("v1:challenge_retrieve", kwargs={"pk": challenge_disabled.pk}),
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
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        response_before_submissions = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response_before_submissions.status_code, 200)
        length_before_adding_submissions = len(
            response_before_submissions.data["results"]
        )

        models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data["results"]), length_before_adding_submissions + 1
        )

    def test_list_submissions_shown_when_submitted(self):
        """Test that logged in users can see submissions that are shown when team has submission for the challenge as
        well."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        response_before_submissions = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response_before_submissions.status_code, 200)
        length_before_adding_submissions = len(
            response_before_submissions.data["results"]
        )

        self.assertEqual(
            models.Submission.objects.filter(
                team=self.normal_user_team,
                accepted=True,
                challenge=self.challenge_show_when_submitted,
            ).count(),
            0,
        )

        models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data["results"]), length_before_adding_submissions
        )

    def test_list_submissions_always_shown_for_own_team(self):
        """Test that logged in users can always see submissions of their own team."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        response_before_submissions = self.client.get(
            reverse("v1:submissions_listcreate"),
            format="json",
        )
        self.assertEqual(response_before_submissions.status_code, 200)
        length_before_adding_submissions = len(
            response_before_submissions.data["results"]
        )

        with self.subTest("Normal challenge not accepted"):
            models.Submission.objects.create(
                challenge=self.challenge,
                tournament=self.test_tournament,
                team=self.normal_user_team,
                file=self.test_file,
                accepted=False,
            )

            response = self.client.get(
                reverse("v1:submissions_listcreate"),
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.data["results"]), length_before_adding_submissions + 1
            )

        with self.subTest("Normal challenge accepted"):
            models.Submission.objects.create(
                challenge=self.challenge,
                tournament=self.test_tournament,
                team=self.normal_user_team,
                file=self.test_file_2,
                accepted=True,
            )

            response = self.client.get(
                reverse("v1:submissions_listcreate"),
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.data["results"]), length_before_adding_submissions + 2
            )

        with self.subTest("Show on accept challenge not accepted"):
            models.Submission.objects.create(
                challenge=self.challenge_show_when_submitted,
                tournament=self.test_tournament,
                team=self.normal_user_team,
                file=self.test_file_3,
                accepted=False,
            )

            response = self.client.get(
                reverse("v1:submissions_listcreate"),
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.data["results"]), length_before_adding_submissions + 3
            )

        with self.subTest("Show on accept challenge accepted"):
            models.Submission.objects.create(
                challenge=self.challenge_show_when_submitted,
                tournament=self.test_tournament,
                team=self.normal_user_team,
                file=self.test_file_4,
                accepted=True,
            )

            response = self.client.get(
                reverse("v1:submissions_listcreate"),
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.data["results"]), length_before_adding_submissions + 4
            )

    def test_create_submission_not_logged_in(self):
        """Test that non logged in users can not create submissions."""
        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": self.test_file,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_create_submission_logged_in(self):
        """Test that logged in users can create submissions."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run + 1
        )

    def test_create_submission_not_in_team(self):
        """Test that logged in users without a team can not create submissions."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.normal_user_team.members.remove(self.normal_user)
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_other_team(self):
        """Test that logged in users with a team can not create submissions for another team."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.test_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_non_existing_challenge(self):
        """Test that logged in users with a team can not create submissions for challenges that do not exist."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )

        submissions_before_run = models.Submission.objects.all().count()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": 10000,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_other_ones_file(self):
        """Test that logged in users with a team can not create submissions with a file belonging to someone else."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )
        self.assertEquals(
            models.Submission.objects.filter(file__id=self.test_file.id).count(), 0
        )

        submissions_before_run = models.Submission.objects.all().count()

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": self.test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_challenge_disabled(self):
        """Test that logged in users with a team can not create submissions for a disabled challenge."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        self.challenge.disabled = True
        self.challenge.save()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_challenge_not_active_yet(self):
        """Test that logged in users with a team can not create submissions for a challenge that is active in the
        future."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        self.challenge.active_until = None
        self.challenge.active_from = timezone.now() + timedelta(days=1)
        self.challenge.save()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_create_submission_challenge_active_in_past(self):
        """Test that logged in users with a team can not create submissions for a challenge that was active in the
        past."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        self.assertEquals(
            models.Submission.objects.filter(
                challenge=self.challenge, team=self.normal_user_team, accepted=True
            ).count(),
            0,
        )

        submissions_before_run = models.Submission.objects.all().count()

        self.challenge.active_from = None
        self.challenge.active_until = timezone.now() - timedelta(days=1)
        self.challenge.save()

        test_file = File.objects.create(
            file=SimpleUploadedFile(name="file", content=b"aksdjflask"),
            original_file_name="test file",
            file_name="test file name",
            file_type="image/photo",
            created_by=self.normal_user,
        )

        response = self.client.post(
            reverse("v1:submissions_listcreate"),
            {
                "challenge": self.challenge.id,
                "team": self.normal_user_team.id,
                "tournament": self.challenge.tournament.id,
                "file": test_file.id,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            models.Submission.objects.all().count(), submissions_before_run
        )

    def test_retrieve_submission_not_logged_in(self):
        """Test that non logged in users can not retrieve submissions."""
        submission_1 = models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        submission_2 = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file_2,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission_1.pk}),
        )

        self.assertEqual(response.status_code, 401)

        response = self.client.get(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission_2.pk}),
        )

        self.assertEqual(response.status_code, 401)

    def test_retrieve_submissions_own_team(self):
        """Test that logged in users can retrieve submissions of their own team."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        submission_1 = models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file,
            accepted=False,
        )

        submission_2 = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file_2,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission_1.pk}),
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission_2.pk}),
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_submissions_other_team(self):
        """Test that logged in users can retrieve submissions of other teams once accepted."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        response = self.client.get(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_submissions_other_team_show_on_accept(self):
        """Test that logged in users can only retrieve submissions of other teams for show on accept challenges once
        they have their own accepted submission."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        submission_other_team = models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=True,
        )

        response = self.client.get(
            reverse(
                "v1:submissions_retrieveupdate", kwargs={"pk": submission_other_team.pk}
            ),
        )

        self.assertEqual(response.status_code, 404)

        submission_own_team = models.Submission.objects.create(
            challenge=self.challenge_show_when_submitted,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file_2,
            accepted=False,
        )

        response = self.client.get(
            reverse(
                "v1:submissions_retrieveupdate", kwargs={"pk": submission_own_team.pk}
            ),
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse(
                "v1:submissions_retrieveupdate", kwargs={"pk": submission_other_team.pk}
            ),
        )

        self.assertEqual(response.status_code, 404)

        submission_own_team.accepted = True
        submission_own_team.save()

        response = self.client.get(
            reverse(
                "v1:submissions_retrieveupdate", kwargs={"pk": submission_other_team.pk}
            ),
        )

        self.assertEqual(response.status_code, 200)

    def test_update_submissions_not_logged_in(self):
        """Test that non logged in users can not update submissions."""
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file,
            accepted=False,
        )

        response = self.client.patch(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
            {"accepted": True},
        )

        self.assertEqual(response.status_code, 401)

    def test_update_submissions_no_rights(self):
        """Test that logged in users without rights can not update submissions."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file,
            accepted=False,
        )

        response = self.client.patch(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
            {"accepted": True},
        )

        self.assertEqual(
            models.Submission.objects.get(pk=submission.pk).accepted, False
        )
        self.assertEqual(response.status_code, 401)

    def test_update_submissions_have_rights(self):
        """Test that logged in users with rights can update submissions."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        content_type = ContentType.objects.get_for_model(models.Submission)
        permission = Permission.objects.get(
            codename="change_submission", content_type=content_type
        )
        self.normal_user.user_permissions.add(permission)
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.normal_user_team,
            file=self.test_file,
            accepted=False,
        )

        response = self.client.patch(
            reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
            {"accepted": True},
        )

        self.assertEqual(models.Submission.objects.get(pk=submission.pk).accepted, True)
        self.assertEqual(response.status_code, 200)

    def test_update_submissions_have_rights_other_team(self):
        """Test that logged in users with rights can update submissions of other teams as well."""
        self.assertTrue(
            self.client.login(username=self.normal_user.username, password="password")
        )
        content_type = ContentType.objects.get_for_model(models.Submission)
        permission = Permission.objects.get(
            codename="change_submission", content_type=content_type
        )
        self.normal_user.user_permissions.add(permission)
        submission = models.Submission.objects.create(
            challenge=self.challenge,
            tournament=self.test_tournament,
            team=self.test_team,
            file=self.test_file,
            accepted=False,
        )

        with self.subTest(
            "Without viewing rights other teams submissions cant be seen or altered"
        ):
            response = self.client.patch(
                reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
                {"accepted": True},
            )

            self.assertEqual(
                models.Submission.objects.get(pk=submission.pk).accepted, False
            )
            self.assertEqual(response.status_code, 404)

        with self.subTest(
            "With viewing rights other teams submissions can be seen and altered"
        ):
            content_type = ContentType.objects.get_for_model(models.Submission)
            permission = Permission.objects.get(
                codename="view_submission", content_type=content_type
            )
            self.normal_user.user_permissions.add(permission)
            response = self.client.patch(
                reverse("v1:submissions_retrieveupdate", kwargs={"pk": submission.pk}),
                {"accepted": True},
            )

            self.assertEqual(
                models.Submission.objects.get(pk=submission.pk).accepted, True
            )
            self.assertEqual(response.status_code, 200)
