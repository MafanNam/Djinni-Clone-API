from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "your_project_name.apps.accounts" # added the project name to the name attribute
    verbose_name = _("Accounts")

    def ready(self):
        # Add any initialization code here, if needed
        pass
