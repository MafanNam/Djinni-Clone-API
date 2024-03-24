import os

from celery import Celery
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.local")

# Initialize Django
django.setup()

# Initialize Celery
app = Celery("backend")

# Configure Celery using settings from Django base.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()

