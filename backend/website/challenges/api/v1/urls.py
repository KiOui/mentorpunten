from django.urls import path
from challenges.api.v1.views import (
    ChallengeListAPIView,
    ChallengeRetrieveAPIView,
    SubmissionListCreateAPIView,
    SubmissionRetrieveUpdateAPIView,
)

urlpatterns = [
    path("", ChallengeListAPIView.as_view(), name="challenge_list"),
    path("<int:pk>/", ChallengeRetrieveAPIView.as_view(), name="challenge_retrieve"),
    path("submissions/", SubmissionListCreateAPIView.as_view(), name="submissions_listcreate"),
    path("submissions/<int:pk>/", SubmissionRetrieveUpdateAPIView.as_view(), name="submissions_retrieveupdate"),
]
