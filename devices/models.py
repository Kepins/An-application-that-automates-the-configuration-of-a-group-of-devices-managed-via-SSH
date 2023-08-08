from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from lazy_import import lazy_module

youtube_models = lazy_module("youtube.models")


class CustomUser(AbstractBaseUser):

    password = models.CharField(max_length=128, required=True)
    #pub_key = models.Forei(max_length=255, unique=True)

