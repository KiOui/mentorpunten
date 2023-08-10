from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from challenges.api.v1 import serializers
from challenges import models
from files.models import File
from mentorpunten.api.v1.pagination import StandardResultsSetPagination


class ChallengeListAPIView(ListAPIView):
    """Challenge List API View."""

    serializer_class = serializers.ChallengeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tournament"]

    def get_queryset(self):
        """Get queryset."""
        return models.Challenge.objects.all()


class ChallengeRetrieveAPIView(RetrieveAPIView):
    """Challenge Retrieve API View."""

    serializer_class = serializers.ChallengeSerializer

    def get_queryset(self):
        """Get queryset."""
        return models.Challenge.objects.revealed_challenges()


class SubmissionFilter(FilterSet):
    """Submission FilterSet."""

    class Meta:
        """Meta class."""

        model = models.Submission
        fields = {
            "accepted": ("exact", "isnull"),
            "challenge": ("exact",),
            "team": ("exact",),
            "created_by": ("exact",),
            "updated_by": ("exact",),
            "tournament": ("exact",),
        }


class SubmissionListCreateAPIView(ListCreateAPIView):
    """Submission List Create API View."""

    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()

    parser_classes = [MultiPartParser, FormParser]

    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubmissionFilter

    def get_queryset(self):
        """
        Get queryset of submissions.

        The displayed queryset depends on whether the user is authenticated.
        """
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(accepted=True) | Q(team__members__in=[self.request.user])
            ).distinct()
        else:
            return self.queryset.filter(accepted=True)

    def create(self, request, *args, **kwargs):
        """Create a submission."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        team_id = request.data.get("team", None)
        possible_teams = models.Team.objects.filter(
            id=team_id, members__in=[request.user]
        )
        if len(possible_teams) == 0:
            # Team does not exist or user is not a member of the team.
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            team = possible_teams[0]

        challenge_id = request.data.get("challenge", None)
        try:
            challenge = models.Challenge.objects.get(id=challenge_id)
        except models.Challenge.DoesNotExist:
            # Challenge does not exist.
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not challenge.active:
            # Challenge is not active.
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif challenge.tournament != team.tournament:
            # Tournament of Challenge and Tournament of Team do not correspond.
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file_id = request.data.get("file", None)
        if file_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            file = File.objects.get(
                id=file_id, created_by=request.user, submission=None
            )
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            data={
                "accepted": None,
                "team": team.id,
                "challenge": challenge.id,
                "tournament": challenge.tournament.id,
                "file": file.id,
                "created_by": request.user.id,
            }
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SubmissionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Submission Retrieve Update API View."""

    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()

    def get_queryset(self):
        """
        Get queryset of submissions.

        The displayed queryset depends on whether the user is authenticated.
        """
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(accepted=True) | Q(team__members__in=[self.request.user])
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
