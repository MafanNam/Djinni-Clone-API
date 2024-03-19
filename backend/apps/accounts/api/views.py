from apps.accounts.api.serializers import CandidateProfileSerializer, UpdateCandidateProfileSerializer
from apps.accounts.models import CandidateProfile
from rest_framework import generics, permissions

from .permissions import CandidateRequiredPermission


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
