# my_app/celery.py
from celery import Celery

app = Celery("my_app")

# my_app/__init__.py
from .celery import app as celery_app

__all__ = ("celery_app",)
