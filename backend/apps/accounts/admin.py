from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from django.contrib import admin

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("candidate_id", "candidate_user", "candidate_first_name", "candidate_last_name", "candidate_skills")
    list_display_links = ("candidate_id", "candidate_user")
    search_fields = ("candidate_first_name", "candidate_last_name")
    list_filter = ("user", "created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("skills")

    def candidate_skills(self, obj):
        return ", ".join(skill.name for skill in obj.skills.all())


models_to_register = (
    (RecruiterProfile, "recruiter_", ("user", "first_name", "last_name")),
    (ContactCv, "contact_", ("user", "first_name", "last_name", "created_at")),
)

for model, prefix, fields in models_to_register:
    @admin.register(model)
    class ModelAdmin(admin.ModelAdmin):
        list_display = (f"{prefix}id", f"{prefix}user", *fields)
        list_display_links = (f"{prefix}id", f"{prefix}user")
        search_fields = (f"{prefix}first_name", f"{prefix}last_name")
        list_filter = (f"{prefix}user", "created_at", "updated_at")
