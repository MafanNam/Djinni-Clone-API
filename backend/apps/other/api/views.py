from apps.accounts.api.permissions import RecruiterRequiredPermission
from rest_framework import generics, permissions, serializers
from rest_framework.generics import get_object_or_404

from ..models import Category, Company
from .serializers import CategorySerializer, CompanySerializer


class CategoryListAPIView(generics.ListAPIView):
    """List all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    """List all companies, or create a new company."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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
