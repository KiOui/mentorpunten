from django.urls import path
<<<<<<< HEAD
from challenges.api.v1.views import ChallengeListAPIView, ChallengeRetrieveAPIView, SubmissionListCreateAPIView, \
    SubmissionRetrieveUpdateAPIView, TeamListAPIView, TeamRetrieveAPIView, ChallengeUserMeAPIView
=======
from challenges.api.v1.views import (
    ChallengeListAPIView,
    ChallengeRetrieveAPIView,
    SubmissionListCreateAPIView,
    SubmissionRetrieveUpdateAPIView,
    TeamListAPIView,
    TeamRetrieveAPIView,
)
>>>>>>> 396b02d739d3b4c84bc8858c468e28fe287e182c

urlpatterns = [
    path("", ChallengeListAPIView.as_view(), name="challenge_list"),
    path("<int:pk>/", ChallengeRetrieveAPIView.as_view(), name="challenge_retrieve"),
<<<<<<< HEAD
    path("submissions/", SubmissionListCreateAPIView.as_view(), name="submissions_listcreate"),
    path("submissions/<int:pk>/", SubmissionRetrieveUpdateAPIView.as_view(), name="submissions_retrieveupdate"),
    path("teams/", TeamListAPIView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamRetrieveAPIView.as_view(), name="team_retrieve"),
    path("users/me/", ChallengeUserMeAPIView.as_view(), name="challengeuser_me_retrieve"),
=======
    path(
        "submissions/",
        SubmissionListCreateAPIView.as_view(),
        name="submissions_listcreate",
    ),
    path(
        "submissions/<int:pk>/",
        SubmissionRetrieveUpdateAPIView.as_view(),
        name="submissions_retrieveupdate",
    ),
    path("teams/", TeamListAPIView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamRetrieveAPIView.as_view(), name="team_retrieve"),
>>>>>>> 396b02d739d3b4c84bc8858c468e28fe287e182c
]
