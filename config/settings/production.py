from .base import *

env = Env()

# SECURITY WARNING: keep the  key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")
FIELD_ENCRYPTION_KEY = env("FIELD_ENCRYPTION_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)
