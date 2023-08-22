from django.contrib.auth.models import AbstractUser
from django.db import models

from .key_pair import KeyPair


class CustomUser(AbstractUser):

    """Key used for ssh authorization"""
    key_pair = models.ForeignKey(KeyPair, null=True, on_delete=models.SET_NULL)
