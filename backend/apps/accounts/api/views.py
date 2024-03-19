from apps.accounts.api.serializers import (
    CandidateProfileSerializer,
    RecruiterProfileSerializer,
    UpdateCandidateProfileSerializer,
)
from apps.accounts.models import CandidateProfile, RecruiterProfile
from rest_framework import generics, permissions

from .permissions import CandidateRequiredPermission, RecruiterRequiredPermission


class CandidateProfileListAPIView(generics.ListAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]


class CandidateProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = CandidateProfile.objects.select_related("user")
        return queryset


class CandidateProfileUserAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [CandidateRequiredPermission]

    def get_object(self):
        candidate_profile = self.request.user.candidate_profile
        return candidate_profile

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CandidateProfileSerializer
        return UpdateCandidateProfileSerializer


class RecruiterProfileListAPIView(generics.ListAPIView):
    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]


class RecruiterProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RecruiterProfile.objects.select_related("user")
        return queryset


class RecruiterProfileUserAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [RecruiterRequiredPermission]
    serializer_class = RecruiterProfileSerializer

    def get_object(self):
        recruiter_profile = self.request.user.recruiter_profile
        return recruiter_profile
