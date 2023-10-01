from django.db import models

from application.models.device import Device
from application.models.key_pair import KeyPair


class Group(models.Model):
    """Model that represents group of devices that could be configured"""

    """Human readable name"""
    name = models.CharField(100)

    """Key used for ssh authorization"""
    key_pair = models.ForeignKey(KeyPair, null=True, on_delete=models.SET_NULL)

    """Devices that are part of this group"""
    devices = models.ManyToManyField(Device, related_name="groups", blank=True)
