from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import OnlineUser, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "type_profile",
        "is_staff",
        "is_active",
    ]

    list_editable = ["is_active"]

    list_display_links = ["id", "email"]

    list_filter = ["email", "type_profile", "is_staff", "is_active"]

    fieldsets = (
        (_("Personal Info"), {"fields": ("first_name", "last_name", "type_profile")}),
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "type_profile",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name"]


@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "last_login")
    list_display_links = ("id", "user")
