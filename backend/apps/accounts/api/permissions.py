from apps.users.models import TYPE_PROFILE_CHOICES
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class RecruiterRequiredPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type_profile == TYPE_PROFILE_CHOICES.recruiter:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CandidateRequiredPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type_profile == TYPE_PROFILE_CHOICES.candidate:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
