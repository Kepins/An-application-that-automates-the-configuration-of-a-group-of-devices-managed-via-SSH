from django.db import models

from application.models.device import Device
from application.models.public_key import PublicKey


class Group(models.Model):
    """Model that represents group of devices that could be configured"""

    """Human readable name"""
    name = models.CharField(40)

    """Key used for ssh authorization"""
    public_key = models.ForeignKey(PublicKey, null=True, on_delete=models.SET_NULL)

    """Devices that are part of this group"""
    devices = models.ManyToManyField(Device, related_name="groups", blank=True)
