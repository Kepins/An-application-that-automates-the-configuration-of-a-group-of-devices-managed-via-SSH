from django.db import models


# Create your models here.
class ModelWithTimestamps(models.Model):
    """Abstract base class for models that require timespamps of creation and modification"""

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublicKey(models.Model):
    """Public ssh-key that has content of ssh-keygen generated file"""

    # class TypeOfKey(models.TextChoices):
    #     DSA = "dsa"
    #     ECDSA = "ecdsa"
    #     ECDSA_SK = "ecdsa-sk"
    #     ED25519 = "ed25519"
    #     ED25519_SK = "ed25519-sk"
    #     RSA = "rsa"

    # type = models.CharField(choices=TypeOfKey.choices)

    """ssh-key file content (That COULD be stripped of the comment at the end)"""
    key_content = models.BinaryField(
        max_length=1024,
        unique=True,
    )  # 1024 is an arbitrary number

    # comment = models.CharField()


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
