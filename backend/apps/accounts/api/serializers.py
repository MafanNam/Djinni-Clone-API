from apps.accounts.models import EMPLOY_OPTIONS, CandidateProfile
from apps.other.models import Category
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

        # def update(self, instance, validated_data):
        #     instance.first_name = validated_data.get("first_name", instance.first_name)
        #     instance.last_name = validated_data.get("last_name", instance.last_name)
        #     instance.position = validated_data.get("position", instance.position)
        #     instance.category = validated_data.get("category", instance.category)
        #     instance.work_exp = validated_data.get("work_exp", instance.work_exp)
        #     instance.work_exp_bio = validated_data.get("work_exp_bio", instance.work_exp_bio)
        #     instance.salary_expectation = validated_data.get("salary_expectation", instance.salary_expectation)
        #     instance.country = validated_data.get("country", instance.country)
        #     instance.city = validated_data.get("city", instance.city)
        #     instance.eng_level = validated_data.get("eng_level", instance.eng_level)
        #     instance.employ_options = validated_data.get("employ_options", instance.employ_options)
        #     instance.image = validated_data.get("image", instance.image)
        #     instance.find_job = validated_data.get("find_job", instance.find_job)
        #
        #     if "skills" in validated_data:
        #         instance.skills.set(validated_data["skills"])
        #
        #     instance.save()
        #
        #     return instance
