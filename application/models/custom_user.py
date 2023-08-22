from django.contrib.auth.models import AbstractUser
from django.db import models

from .public_key import PublicKey


class CustomUser(AbstractUser):

    """Key used for ssh authorization"""

    public_key = models.ForeignKey(PublicKey, null=True, on_delete=models.SET_NULL)
