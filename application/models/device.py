from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from encrypted_model_fields import fields

from .key_pair import KeyPair


class Device(models.Model):
    """Model that represents device that could be configured"""

    """Human readable name"""
    name = models.CharField(100)

    """Account name on device"""
    username = models.CharField(255)

    """Hostname or IPv4 or IPv6"""
    hostname = models.CharField(
        255
    )  # 255 characters is maximum for hostname as well as models.CharField

    """Port on which device listens"""
    port = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
        default=22,
    )

    """Keys used for ssh authorization"""
    key_pair = models.ForeignKey(KeyPair, null=True, on_delete=models.SET_NULL)

    """Password"""
    password = fields.EncryptedCharField(255, null=True)

    """Device public key to prevent MitM attacks"""
    public_key = models.TextField(db_index=False, null=True)
