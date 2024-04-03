from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

User = get_user_model()


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # token["user"] = CustomUserSerializer(user).data
#
#         return token

# def validate(self, attrs):
#     data = super().validate(attrs)
#
#     data.update({
#         'user': CustomUserSerializer(self.user).data
#     })
#     return data


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "email", "password")


class CustomUserSerializer(UserSerializer):
    type_profile = serializers.CharField(source="get_type_profile_display", read_only=True)
    is_online = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "email", "is_online")
        read_only_fields = ("email", "type_profile")

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_online(self, obj):
        if hasattr(obj, "online_user"):
            return obj.online_user.is_online()
        return False


class ShortCustomUserSerializer(CustomUserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "is_online")
