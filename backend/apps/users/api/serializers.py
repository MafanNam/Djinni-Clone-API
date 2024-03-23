from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "email", "password")


class CustomUserSerializer(UserSerializer):
    type_profile = serializers.CharField(source="get_type_profile_display", read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "email")
        read_only_fields = ("email", "type_profile")


class ShortCustomUserSerializer(CustomUserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile")
