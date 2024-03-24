from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.api.urls', namespace='accounts-api')),
]

# apps/accounts/api/urls.py
from django.urls import path
from .views import (
    CandidateProfileListAPIView,
    CandidateProfileDetailAPIView,
    CandidateProfileUserAPIView,
    ContactCvDetailAPIView,
    RecruiterProfileListAPIView,
    RecruiterProfileDetailAPIView,
    RecruiterProfileUserAPIView,
)

app_name = 'accounts-api'
urlpatterns = [
    path('candidates/', CandidateProfileListAPIView.as_view(), name='candidate-list'),
    path('candidates/<int:pk>/', CandidateProfileDetailAPIView.as_view(), name='candidate-detail'),
    path('candidates/me/', CandidateProfileUserAPIView.as_view(), name='candidate-me'),
    path('candidates/me/cv/', ContactCvDetailAPIView.as_view(), name='candidate-cv'),
    path('recruiters/', RecruiterProfileListAPIView.as_view(), name='recruiter-list'),
    path('recruiters/<int:pk>/', RecruiterProfileDetailAPIView.as_view(), name='recruiter-detail'),
    path('recruiters/me/', RecruiterProfileUserAPIView.as_view(), name='recruiter-me'),
]
