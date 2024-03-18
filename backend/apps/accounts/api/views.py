from apps.accounts.api.serializers import CandidateProfileSerializer
from apps.accounts.models import CandidateProfile
from rest_framework import generics, permissions


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

    def get_object(self):
        id = self.kwargs["pk"]
        candidate_profile = self.get_queryset().get(id=id)
        return candidate_profile
