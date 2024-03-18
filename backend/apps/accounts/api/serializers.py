from apps.accounts.models import EMPLOY_OPTIONS, CandidateProfile
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
