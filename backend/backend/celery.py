import os

from celery import Celery
from django.conf import settings
from environ import Env

env = Env()

# TODO: change this in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE", default="backend.settings.local"))
app = Celery("backend")

# Configure Celery using settings from Django base.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
