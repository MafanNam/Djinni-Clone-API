from apps.accounts.api.serializers import (
    CandidateProfileSerializer,
    ContactCvSerializer,
    ShortRecruiterProfileSerializer,
)
from apps.accounts.models import EMPLOY_OPTIONS
from apps.core.serializers import CustomMultipleChoiceField
from apps.other.api.serializers import ShortCompanySerializer
from apps.other.models import Category, Company
from apps.vacancy.models import Feedback, Vacancy
from django_countries.serializer_fields import CountryField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField


class UpdateVacancySerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    company = serializers.SlugRelatedField(slug_field="name", queryset=Company.objects.all())
    recruiter = serializers.SerializerMethodField()
    views = serializers.IntegerField(source="vacancy_views.count", read_only=True)
    feedback = serializers.IntegerField(source="feedback_vacancy.count", read_only=True)
    is_user_feedback = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "recruiter",
            "company",
            "title",
            "slug",
            "description",
            "requirements",
            "other",
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
            "is_user_feedback",
            "created_at",
            "updated_at",
        )
        depth = 1

    @extend_schema_field(ShortRecruiterProfileSerializer)
    def get_recruiter(self, obj):
        return ShortRecruiterProfileSerializer(
            obj.user.recruiter_profile, context={"request": self.context["request"]}, many=False
        ).data

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_user_feedback(self, obj):
        if not self.context["request"].user.is_authenticated:
            return False
        return Feedback.objects.filter(user=self.context["request"].user, vacancy=obj).exists()


class RetrieveVacancySerializer(UpdateVacancySerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    company = ShortCompanySerializer(read_only=True, many=False)


class VacancySerializer(UpdateVacancySerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    country = CountryField(name_only=True)
    eng_level = serializers.CharField(source="get_eng_level_display", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    company = ShortCompanySerializer(read_only=True, many=False)


# class UpdateMyVacancySerializer(UpdateVacancySerializer):
#     country = CountryField(name_only=False)
#     category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())


class ShortVacancySerializer(UpdateVacancySerializer):
    class Meta:
        model = Vacancy
        fields = (
            "slug",
            "title",
            "company",
            "employ_options",
            "created_at",
            "updated_at",
        )


class FeedbackSerializer(serializers.ModelSerializer):
    candidate = serializers.SerializerMethodField()
    contact_cv = ContactCvSerializer(read_only=True, many=False)
    vacancy = ShortVacancySerializer(read_only=True, many=False)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "candidate",
            "vacancy",
            "contact_cv",
            "cover_letter",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(CandidateProfileSerializer)
    def get_candidate(self, obj):
        return CandidateProfileSerializer(
            obj.user.candidate_profile, context={"request": self.context["request"]}, many=False
        ).data


class ShortFeedbackSerializer(FeedbackSerializer):
    contact_cv = ContactCvSerializer(read_only=True, many=False)

    class Meta:
        model = Feedback
        fields = (
            "vacancy",
            "contact_cv",
        )
