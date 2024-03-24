from apps.accounts.api.permissions import RecruiterRequiredPermission
from rest_framework import generics, permissions, serializers

from .models import Category, Company
from .serializers import CategorySerializer, CompanySerializer


class CategoryListAPIView(generics.ListAPIView):
    """List all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CompanyMixin:
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        user = self.request.user
        if Company.objects.filter(user=user).exists():
            raise serializers.ValidationError({"message": "Company already exists"})
        serializer.save(user=user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [RecruiterRequiredPermission]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CompanyListCreateAPIView(CompanyMixin, generics.ListCreateAPIView):
    """List all companies, or create a new company."""


class CompanyDetailAPIView(CompanyMixin, generics.RetrieveUpdateDestroyAPIView):
    """CRUD view for company details. Only recruiters can edit or delete companies."""
