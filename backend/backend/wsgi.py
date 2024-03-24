"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Append the local settings module if it exists
if os.path.exists(os.path.join(os.path.dirname(__file__), "settings", "local.py")):
    os.environ["DJANGO_SETTINGS_MODULE"] += ".local"

# Initialize the WSGI application
application = get_wsgi_application()
