from apps.vacancy.models import Feedback, Vacancy, VacancyView
from django.contrib import admin

@admin.register(VacancyView)
class VacancyViewAdmin(admin.ModelAdmin):
    list_display = ["id", "vacancy", "user", "viewer_ip", "created_at", "updated_at"]
    list_display_links = ["id", "vacancy"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["vacancy", "user", "viewer_ip"]
    readonly_fields = ["vacancy", "user", "viewer_ip", "created_at", "updated_at"]
    date_hierarchy = 'created_at'

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "company", "salary", "country", "created_at"]
    list_display_links = ["id", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user", "title", "company", "country"]
    readonly_fields = ["user", "title", "company", "salary", "country", "created_at"]
    date_hierarchy = 'created_at'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "vacancy", "created_at"]
    list_display_links = ["id", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user", "vacancy"]
    readonly_fields = ["user", "vacancy", "created_at"]
    date_hierarchy = 'created_at'
