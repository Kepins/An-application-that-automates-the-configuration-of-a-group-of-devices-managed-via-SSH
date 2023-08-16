from django.db import models

from .PublicKey import PublicKey


class Device(models.Model):
    """Model that represents device that could be configured"""

    """Human readable name"""
    name = models.CharField(40)

    """Hostname or IPv4 or IPv6"""
    hostname = models.CharField(
        255
    )  # 255 characters is maximum for hostname as well as models.CharField

    """Key used for ssh authorization"""
    public_key = models.ForeignKey(PublicKey, null=True, on_delete=models.SET_NULL)
