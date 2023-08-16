from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from lazy_import import lazy_module

youtube_models = lazy_module("youtube.models")



class CustomUser(AbstractUser):

    pass




