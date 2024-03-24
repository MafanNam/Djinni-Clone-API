from django.apps import AppConfig
import apps.users.signals  # import signals module here to avoid lazy initialization
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = _("Users")

    def ready(self):
        # Connect signals after all models have been loaded
        from django.db import models
        from django.contrib.auth.models import Group as AuthGroup
        from django.contrib.contenttypes.models import ContentType

        # Ensure User and AuthGroup models are loaded before initializing signals
        models.load_model('auth.User')
        models.load_model(AuthGroup)

        apps.users.signals.connect_signals(
            ContentType,
            models.User,
            AuthGroup
        )

