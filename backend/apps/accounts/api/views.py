from apps.accounts.api.serializers import (
    CandidateProfileSerializer,
    ContactCvSerializer,
    RecruiterProfileSerializer,
    UpdateCandidateProfileSerializer,
    UpdateRecruiterProfileSerializer,
)
from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from django.http import Http404
from rest_framework import generics, permissions, filters, throttling

from .permissions import CandidateRequiredPermission, RecruiterRequiredPermission


class CandidateProfileListAPIView(generics.ListAPIView):
    """List Candidate Profiles"""

    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = generics.PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name", "user__last_name"]
    search_fields = ["user__first_name", "user__last_name"]
    throttle_classes = [throttling.AnonRateThrottle, throttling.UserRateThrottle]


class CandidateProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Candidate Profile"""

    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"
    lookup_url_kwarg = "candidate_profile_id"

    def get_queryset(self):
        queryset = CandidateProfile.objects.select_related("user")
        return queryset


class CandidateProfileUserAPIView(generics.RetrieveUpdateAPIView):
    """Detail Update Candidate Profile. Only candidate can edit profile."""

    permission_classes = [CandidateRequiredPermission]
    lookup_field = "pk"
    lookup_url_kwarg = "candidate_profile_id"

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
    pagination_class = generics.PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name", "user__last_name"]
    search_fields = ["user__first_name", "user__last_name"]
    throttle_classes = [throttling.AnonRateThrottle, throttling.UserRateThrottle]


class RecruiterProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Recruiter Profile"""

    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"
    lookup_url_kwarg = "recruiter_profile_id"

    def get_queryset(self):
        queryset = RecruiterProfile.objects.select_related("user")
        return queryset


class RecruiterProfileUserAPIView(generics.RetrieveUpdateAPIView):
    """Detail Update Recruiter Profile. Only recruiter can edit profile."""

    permission_classes = [RecruiterRequiredPermission]
    lookup_field = "pk"
    lookup_url_kwarg = "recruiter_profile_id"

    def get_object(self):
        recruiter_profile = self.request.user.recruiter_profile
        return recruiter_profile

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecruiterProfileSerializer
        return UpdateRec
