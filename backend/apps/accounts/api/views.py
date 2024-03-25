from apps.accounts.api.serializers import (
    CandidateProfileSerializer,
    ContactCvSerializer,
    RecruiterProfileSerializer,
    UpdateCandidateProfileSerializer,
    UpdateRecruiterProfileSerializer,
)
from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from django.http import Http404
from rest_framework import generics, permissions

from .permissions import CandidateRequiredPermission, RecruiterRequiredPermission


class CandidateProfileListAPIView(generics.ListAPIView):
    """List Candidate Profiles"""

    queryset = CandidateProfile.objects.select_related("category").prefetch_related("skills").all()
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]


class CandidateProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Candidate Profile"""

    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = CandidateProfile.objects.select_related("user")
        return queryset


class CandidateProfileUserAPIView(generics.RetrieveUpdateAPIView):
    """Detail Update Candidate Profile. Only candidate can edit profile."""

    permission_classes = [CandidateRequiredPermission]

    def get_object(self):
        candidate_profile = self.request.user.candidate_profile
        return candidate_profile

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CandidateProfileSerializer
        return UpdateCandidateProfileSerializer


class RecruiterProfileListAPIView(generics.ListAPIView):
    """List Recruiter Profiles"""

    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]


class RecruiterProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Recruiter Profile"""

    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RecruiterProfile.objects.select_related("user")
        return queryset


class RecruiterProfileUserAPIView(generics.RetrieveUpdateAPIView):
    """Detail Update Recruiter Profile. Only recruiter can edit profile."""

    permission_classes = [RecruiterRequiredPermission]

    def get_object(self):
        recruiter_profile = self.request.user.recruiter_profile
        return recruiter_profile

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecruiterProfileSerializer
        return UpdateRecruiterProfileSerializer


class ContactCvDetailAPIView(generics.RetrieveUpdateAPIView):
    """Detail Contact Cv. Only candidate can edit contact details."""

    permission_classes = [CandidateRequiredPermission]
    serializer_class = ContactCvSerializer

    def get_object(self):
        try:
            contact_cv = self.request.user.contact_cv
        except ContactCv.DoesNotExist:
            raise Http404
        return contact_cv
