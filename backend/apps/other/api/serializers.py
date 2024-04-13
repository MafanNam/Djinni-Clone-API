from apps.other.models import Category, Company
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from taggit.models import Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ShortCompanySerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "image", "bio", "company_url", "country"]


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "image",
            "bio",
            "company_url",
            "dou_url",
            "country",
            "num_employees",
            "created_at",
        ]


class CompanySerializer(CompanyUpdateSerializer):
    country = CountryField(name_only=True)


class SkillsSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source="name")

    class Meta:
        model = Tag
        fields = ["id", "text"]
