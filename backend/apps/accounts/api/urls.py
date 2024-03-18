from apps.accounts.api.views import CandidateProfileDetailAPIView, CandidateProfileListAPIView
from django.urls import path

urlpatterns = [
    path("candidates/", CandidateProfileListAPIView.as_view()),
    path("candidates/<int:pk>/", CandidateProfileDetailAPIView.as_view()),
]
