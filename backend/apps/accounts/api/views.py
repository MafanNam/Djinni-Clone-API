from apps.accounts.api.serializers import (
    CandidateProfileListSerializer,
    CandidateProfileSerializer,
    ContactCvSerializer,
    OfferSerializer,
    RecruiterProfileSerializer,
    UpdateCandidateProfileImageSerializer,
    UpdateCandidateProfileSerializer,
    UpdateContactCvFileSerializer,
    UpdateRecruiterProfileImageSerializer,
    UpdateRecruiterProfileSerializer,
)
from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from apps.core import filters, pagination
from django.contrib.auth import get_user_model
from django.http import Http404
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser

from ...vacancy.models import Offer
from .permissions import CandidateRequiredPermission, RecruiterRequiredPermission

User = get_user_model()


class CandidateProfileListAPIView(generics.ListAPIView):
    """List Candidate Profiles. Pagination page size is 10."""

    queryset = CandidateProfile.objects.select_related("category").prefetch_related("skills").all()
    serializer_class = CandidateProfileListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.MinimumResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.CandidateProfileFilter


class CandidateProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Candidate Profile"""

    serializer_class = CandidateProfileListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = CandidateProfile.objects.select_related("user", "category")
        return queryset


class CandidateOfferAPIView(generics.CreateAPIView):
    """Create Candidate Offer. Only recruiter can create offer."""

    permission_classes = [RecruiterRequiredPermission]
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        user = self.request.user
        candidate = get_object_or_404(User, id=self.kwargs["pk"])
        if Offer.objects.filter(user=user, candidate=candidate).exists():
            raise serializers.ValidationError({"message": "Offer already exists"})
        serializer.save(user=user, candidate=candidate)


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


class CandidateProfileImageUserAPIView(generics.UpdateAPIView):
    """Detail Update Candidate Profile. Only candidate can edit profile."""

    serializer_class = UpdateCandidateProfileImageSerializer
    permission_classes = [CandidateRequiredPermission]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        candidate_profile = self.request.user.candidate_profile
        return candidate_profile


class RecruiterProfileListAPIView(generics.ListAPIView):
    """List Recruiter Profiles. Pagination page size is 10."""

    queryset = RecruiterProfile.objects.select_related("company").all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.MinimumResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.RecruiterProfileFilter


class RecruiterProfileDetailAPIView(generics.RetrieveAPIView):
    """Detail Recruiter Profile"""

    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RecruiterProfile.objects.select_related("user", "company")
        return queryset


class RecruiterProfileUserAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the recruiter profile.

    This class allows authenticated recruiters to view and edit their profile.
    """

    permission_classes = [RecruiterRequiredPermission]

    def get_object(self):
        recruiter_profile = self.request.user.recruiter_profile
        return recruiter_profile

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecruiterProfileSerializer
        return UpdateRecruiterProfileSerializer


class RecruiterProfileImageUserAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the recruiter profile image.

    This class allows authenticated recruiters to view and edit their profile.
    """

    permission_classes = [RecruiterRequiredPermission]
    serializer_class = UpdateRecruiterProfileImageSerializer

    def get_object(self):
        recruiter_profile = self.request.user.recruiter_profile
        return recruiter_profile


class ContactCvDetailAPIView(generics.RetrieveUpdateAPIView):
    """Detail Contact Cv. Only candidate can edit contact details."""

    permission_classes = [CandidateRequiredPermission]
    serializer_class = ContactCvSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        try:
            contact_cv = self.request.user.contact_cv
        except ContactCv.DoesNotExist:
            raise Http404
        return contact_cv


class UpdateContactCvFileAPIView(ContactCvDetailAPIView):
    """Detail Update Contact Cv File. Only candidate can edit contact details."""

    serializer_class = UpdateContactCvFileSerializer
