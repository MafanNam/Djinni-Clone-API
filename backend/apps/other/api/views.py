from apps.accounts.api.permissions import RecruiterRequiredPermission
from rest_framework import generics, permissions, serializers

from ..models import Category, Company
from .serializers import CategorySerializer, CompanySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        user = self.request.user
        if Company.objects.filter(user=user).exists():
            raise serializers.ValidationError({"message": "Company already exists"})
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [RecruiterRequiredPermission]
        elif self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
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
