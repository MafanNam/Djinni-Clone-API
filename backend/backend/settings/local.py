from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY", default="django-insecure-kdxyc)gjt4qs-sk^##l54mrxczdv_)jm%_fg$)5_5bktcmt&ia")

DEBUG = env("DEBUG", default=True)

# if DEBUG:
#     # `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
#     INTERNAL_IPS = type("c", (), {"__contains__": lambda *a: True})()

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    # TODO: Delete JWTFromCookieMiddleware
    "apps.users.middleware.JWTFromCookieMiddleware",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# EMAIL
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = "Djinni Clone <djinniclone@gmail.com>"

# DEBUG TOOLBAR
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "cachalot.panels.CachalotPanel",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: True,
}
