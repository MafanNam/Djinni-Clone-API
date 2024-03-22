from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from django.contrib import admin


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "skill_list")
    list_display_links = ("id", "user")
    search_fields = ("first_name", "last_name")
    list_filter = ("user", "created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("skills")

    def skill_list(self, obj):
        return ", ".join(skill.name for skill in obj.skills.all())


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name")
    list_display_links = ("id", "user")
    search_fields = ("first_name", "last_name")
    list_filter = ("user", "created_at", "updated_at")


@admin.register(ContactCv)
class ContactCvAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "created_at")
    list_display_links = ("id", "user")
    search_fields = ("first_name", "last_name")
    list_filter = ("user", "created_at", "updated_at")
