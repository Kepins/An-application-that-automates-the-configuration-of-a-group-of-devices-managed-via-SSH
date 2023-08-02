"""
ASGI config for ssh_configuration_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

dirname = os.path.dirname
load_dotenv(os.path.join(dirname(dirname(__file__)), ".env"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssh_configuration_app.settings")

application = get_asgi_application()

