from apps.accounts.api.permissions import RecruiterRequiredPermission
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from taggit.models import Tag

from ...core import pagination
from ..models import Category, Company
from .serializers import CategorySerializer, CompanySerializer, CompanyUpdateSerializer, SkillsSerializer


class CategoryListAPIView(generics.ListAPIView):
    """List all categories. Pagination page size is 50."""

    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.LargeResultsSetPagination


class CompanyListAPIView(generics.ListAPIView):
    """List all companies, Pagination page size is 20. Public permission"""

    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    pagination_class = pagination.StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]


class CompanyMyListCreateAPIView(generics.ListCreateAPIView):
    """List user companies and create new, Only 10 companies. Only recruiters can create and list companies."""

    # serializer_class = CompanySerializer
    permission_classes = [RecruiterRequiredPermission]
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "country"]
    ordering_fields = ["created_at", "num_employees"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanySerializer
        return CompanyUpdateSerializer

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        user = self.request.user
        if Company.objects.filter(user=user).count() >= 10:
            raise serializers.ValidationError({"msg": "One Recruiter can only have 10 companies."})
        serializer.save(user=self.request.user)


class CompanyDetailAPIView(generics.RetrieveAPIView):
    """Retrieve view for company details. Public permission"""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class CompanyMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """CRUD view for company details. Only recruiters can update and delete."""

    serializer_class = CompanyUpdateSerializer
    permission_classes = [RecruiterRequiredPermission]

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


class SkillsListAPIView(generics.ListAPIView):
    queryset = Tag.objects.order_by("name").all()
    serializer_class = SkillsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.LargeResultsSetPagination
