from django import get_version

VERSION = (0, 1, 0, "alpha", 0)

__version__ = get_version(VERSION)

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ("celery_app",)
