from apps.accounts.models import EMPLOY_OPTIONS, CandidateProfile, RecruiterProfile
from apps.other.api.serializers import ShortCompanySerializer
from apps.other.models import Category, Company
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField


class CustomMultipleChoiceField(serializers.MultipleChoiceField):
    def to_representation(self, value):
        return {self.choices[item] for item in value}


class CandidateProfileSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.CharField(source="category.name", read_only=True)
    find_job = serializers.CharField(source="get_find_job_display", read_only=True)
    eng_level = serializers.CharField(source="get_eng_level_display", read_only=True)
    country = CountryField(name_only=True)

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "category",
            "skills",
            "work_exp",
            "work_exp_bio",
            "salary_expectation",
            "country",
            "city",
            "eng_level",
            "employ_options",
            "image",
            "find_job",
            "created_at",
            "updated_at",
        )


class UpdateCandidateProfileSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    country = CountryField(name_only=True)

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "category",
            "skills",
            "work_exp",
            "work_exp_bio",
            "salary_expectation",
            "country",
            "city",
            "eng_level",
            "employ_options",
            "image",
            "find_job",
        )


class RecruiterProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    trust_hr = serializers.BooleanField(read_only=True)
    company = ShortCompanySerializer(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "country",
            "company",
            "image",
            "trust_hr",
            "created_at",
            "updated_at",
        )


class UpdateRecruiterProfileSerializer(RecruiterProfileSerializer):
    company = serializers.SlugRelatedField(slug_field="name", queryset=Company.objects.all())
