from apps.accounts.api import views
from django.urls import path

urlpatterns = [
    path("candidates/", views.CandidateProfileListAPIView.as_view()),
    path("candidates/<int:pk>/", views.CandidateProfileDetailAPIView.as_view()),
    path("candidates/me/", views.CandidateProfileUserAPIView.as_view()),
]
