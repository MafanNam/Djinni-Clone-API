from apps.accounts.api import views
from django.urls import path

urlpatterns = [
    path("candidates/", views.CandidateProfileListAPIView.as_view()),
    path("candidates/<int:pk>/", views.CandidateProfileDetailAPIView.as_view()),
    path("candidates/me/", views.CandidateProfileUserAPIView.as_view()),
    path("candidates/me/image/", views.CandidateProfileImageUserAPIView.as_view()),
    path("candidates/me/cv/", views.ContactCvDetailAPIView.as_view()),
    path("candidates/me/cv/file/", views.UpdateContactCvFileAPIView.as_view()),
    path("recruiters/", views.RecruiterProfileListAPIView.as_view()),
    path("recruiters/<int:pk>/", views.RecruiterProfileDetailAPIView.as_view()),
    path("recruiters/me/", views.RecruiterProfileUserAPIView.as_view()),
    path("recruiters/me/image/", views.RecruiterProfileImageUserAPIView.as_view()),
]
