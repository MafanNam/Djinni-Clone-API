from django.apps import AppConfig
import apps.vacancy.signals  # import signals at the top of the file
from django.utils.translation import gettext_lazy as _

class VacancyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.vacancy"
    verbose_name = _("Vacancy")

    def ready(self):
        # Connect signals in the ready method
        apps.vacancy.signals.connect_signals()
