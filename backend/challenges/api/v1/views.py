from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from challenges.api.v1 import serializers
from challenges import models
from challenges.api.v1.serializers import ChallengeUserSerializer
from challenges.models import ChallengeUser
from mentorpunten.api.permissions import IsAuthenticatedOrTokenHasScopeForMethod


class ChallengeListAPIView(ListAPIView):
    """Challenge List API View."""

    serializer_class = serializers.ChallengeSerializer
    queryset = models.Challenge.objects.all()

    def get_queryset(self):
        """Get only the Challenges that are currently active or were active in the past."""
        current_time = timezone.now()
        return self.queryset.filter(
            Q(disabled=False) &
            (
                    Q(active_from=None) |
                    Q(active_from__lt=current_time)
            )
        )


class ChallengeRetrieveAPIView(RetrieveAPIView):
    """Challenge Retrieve API View."""

    serializer_class = serializers.ChallengeSerializer
    queryset = models.Challenge.objects.all()

    def get_queryset(self):
        """Get only the Challenges that are currently active or were active in the past."""
        current_time = timezone.now()
        return self.queryset.filter(
            Q(disabled=False) &
            (
                    Q(active_from=None) |
                    Q(active_from__lt=current_time)
            )
        )


class TeamListAPIView(ListAPIView):
    """Team List API View."""

    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()


class TeamRetrieveAPIView(RetrieveAPIView):
    """Team Retrieve API View."""

    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()


class SubmissionListCreateAPIView(ListCreateAPIView):
    """Submission List Create API View."""

    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["challenge", "team", "accepted"]

    def get_queryset(self):
        """
        Get queryset of submissions.

        The displayed queryset depends on whether the user is authenticated.
        """
        if self.request.user.is_authenticated and self.request.user.challenge_user is not None and self.request.user.challenge_user.team is not None:
            return self.queryset.filter(
                Q(accepted=True) | Q(team=self.request.user.challenge_user.team)
            )
        else:
            return self.queryset.filter(accepted=True)

    def create(self, request, *args, **kwargs):
        """Create a submission."""
        if self.request.user.challenge_user is None or self.request.user.challenge_user.team is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        challenge_id = request.data.get("challenge", None)

        try:
            challenge = models.Challenge.objects.get(id=challenge_id)
        except models.Challenge.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not challenge.active:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={
            "accepted": None,
            "team": self.request.user.challenge_user.team.id,
            "challenge": challenge.id,
            "image": request.data.get("image")
        })

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Submission Retrieve Update API View."""

    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()

    def get_queryset(self):
        """
        Get queryset of submissions.

        The displayed queryset depends on whether the user is authenticated.
        """
        if self.request.user.is_authenticated and self.request.user.challenge_user is not None and self.request.user.challenge_user.team is not None:
            return self.queryset.filter(
                Q(accepted=True) | Q(team=self.request.user.challenge_user.team)
            )
        else:
            return self.queryset.filter(accepted=True)

    def update(self, request, *args, **kwargs):
        """Update a submission."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.has_perm("challenges.update_submission"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)


class ChallengeUserMeAPIView(RetrieveAPIView):
    """
    Me Retrieve API View.

    Permission required: read

    Use this API view to get details about the currently logged in User.
    """

    serializer_class = ChallengeUserSerializer
    queryset = ChallengeUser.objects.all()
    permission_classes = [IsAuthenticatedOrTokenHasScopeForMethod]
    required_scopes_for_method = {
        "GET": ["read"],
    }

    def get_object(self):
        """Get the current logged-in User."""
        try:
            return self.queryset.get(user=self.request.user)
        except ChallengeUser.DoesNotExist:
            raise Http404()
