import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from environ import Env

env = Env()

# TODO: change this in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE", default="backend.settings.local"))
app = Celery("backend")

# Configure Celery using settings from Django base.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "spam-mail-every-week": {
        "task": "apps.users.tasks.send_spam_email_celery_task",
        "schedule": crontab(hour="8", minute="0", day_of_week="mon"),
    }
}

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
