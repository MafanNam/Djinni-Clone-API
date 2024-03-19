from apps.users.models import TYPE_PROFILE_CHOICES
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class RecruiterRequiredPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type_profile == TYPE_PROFILE_CHOICES.employer:
                return True
        return False


class CandidateRequiredPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type_profile == TYPE_PROFILE_CHOICES.candidate:
                return True
        return False
