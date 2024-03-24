from apps.other.models import Category, Company
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class BaseCompanySerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:

