from apps.accounts.api.serializers import (
    CandidateProfileSerializer,
    ContactCvSerializer,
    ShortRecruiterProfileSerializer,
)
from apps.accounts.models import EMPLOY_OPTIONS
from apps.core.serializers import CustomMultipleChoiceField
from apps.other.api.serializers import ShortCompanySerializer
from apps.vacancy.models import Feedback, Vacancy, VacancyView
from django_countries.serializer_fields import CountryField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField


class VacancySerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.CharField(source="category.name", read_only=True)
    eng_level = serializers.CharField(source="get_eng_level_display", read_only=True)
    country = CountryField(name_only=True)
    company = ShortCompanySerializer(read_only=True, many=False)
    recruiter = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    feedback = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "recruiter",
            "company",
            "title",
            "slug",
            "description",
            "eng_level",
            "salary",
            "category",
            "skills",
            "work_exp",
            "employ_options",
            "country",
            "is_only_ukraine",
            "is_test_task",
            "views",
            "feedback",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_views(self, obj):
        return VacancyView.objects.filter(vacancy=obj).count()

    @extend_schema_field(ShortRecruiterProfileSerializer)
    def get_recruiter(self, obj):
        return ShortRecruiterProfileSerializer(
            obj.user.recruiter_profile, context={"request": self.context["request"]}, many=False
        ).data

    @extend_schema_field(OpenApiTypes.INT)
    def get_feedback(self, obj):
        return Feedback.objects.filter(vacancy=obj).count()


class FeedbackSerializer(serializers.ModelSerializer):
    candidate = serializers.SerializerMethodField()
    contact_cv = ContactCvSerializer(read_only=True, many=False)
    vacancy = serializers.CharField(source="vacancy.title", read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "candidate",
            "vacancy",
            "contact_cv",
            "cover_letter",
            "is_bookmark",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(CandidateProfileSerializer)
    def get_candidate(self, obj):
        return CandidateProfileSerializer(
            obj.user.candidate_profile, context={"request": self.context["request"]}, many=False
        ).data
