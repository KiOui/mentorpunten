from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from challenges.api.v1 import serializers
from challenges import models
from mentorpunten.api.v1.pagination import StandardResultsSetPagination


class ChallengeListAPIView(ListAPIView):
    """Challenge List API View."""

    serializer_class = serializers.ChallengeSerializer
    queryset = models.Challenge.objects.revealed_challenges()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tournament"]


class ChallengeRetrieveAPIView(RetrieveAPIView):
    """Challenge Retrieve API View."""

    serializer_class = serializers.ChallengeSerializer
    queryset = models.Challenge.objects.revealed_challenges()


class SubmissionListCreateAPIView(ListCreateAPIView):
    """Submission List Create API View."""

    serializer_class = serializers.SubmissionSerializer
    queryset = models.Submission.objects.all()

    parser_classes = [MultiPartParser, FormParser]

    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["challenge", "team", "accepted", "created_by", "updated_by", "tournament"]

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

    def create(self, request, *args, **kwargs):
        """Create a submission."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        team_id = request.data.get("team", None)
        try:
            team = models.Team.objects.get(id=team_id, members__in=[request.user])
        except models.Team.DoesNotExist:
            # Team does not exist or user is not a member of the team.
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

        serializer = self.get_serializer(data={
            "accepted": None,
            "team": team.id,
            "challenge": challenge.id,
            "tournament": challenge.tournament,
            "image": request.data.get("image"),
            "created_by": request.user,
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
