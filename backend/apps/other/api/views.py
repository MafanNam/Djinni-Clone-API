from apps.accounts.api.permissions import RecruiterRequiredPermission
from rest_framework import generics, permissions, serializers
from rest_framework.generics import get_object_or_404
from taggit.models import Tag

from ...core import pagination
from ..models import Category, Company
from .serializers import CategorySerializer, CompanySerializer, SkillsSerializer


class CategoryListAPIView(generics.ListAPIView):
    """List all categories. Pagination page size is 50."""

    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.LargeResultsSetPagination


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    """List all companies, or create a new company. Pagination page size is 20."""

    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    pagination_class = pagination.StandardResultsSetPagination

    def perform_create(self, serializer):
        user = self.request.user
        if Company.objects.filter(user=user).exists():
            raise serializers.ValidationError({"message": "Company already exists"})
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        company = get_object_or_404(Company, user=request.user)

        recruiter_profile = request.user.recruiter_profile
        recruiter_profile.company = company
        recruiter_profile.save()

        return response

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [RecruiterRequiredPermission]
        elif self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """CRUD view for company details. Only recruiters can edit or delete companies."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [RecruiterRequiredPermission]
        return super().get_permissions()


class SkillsListAPIView(generics.ListAPIView):
    queryset = Tag.objects.order_by("name").all()
    serializer_class = SkillsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.LargeResultsSetPagination
