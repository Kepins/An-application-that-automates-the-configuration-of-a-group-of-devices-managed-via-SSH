from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .public_key import PublicKey


class Device(models.Model):
    """Model that represents device that could be configured"""

    """Human readable name"""
    name = models.CharField(40)

    """Hostname or IPv4 or IPv6"""
    hostname = models.CharField(
        255
    )  # 255 characters is maximum for hostname as well as models.CharField

    """Port on which device listens"""
    port = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
        default=22,
    )

    """Key used for ssh authorization"""
    public_key = models.ForeignKey(PublicKey, null=True, on_delete=models.SET_NULL)

    """Password"""
    password = models.CharField(255, null=True)
