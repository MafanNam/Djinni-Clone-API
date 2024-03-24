from apps.other.models import Category, Company
from django.contrib import admin

class MyModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 20

@admin.register(Company)
class CompanyAdmin(MyModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(MyModelAdmin):
    pass
