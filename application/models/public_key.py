from django.db import models


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
    key_content = models.TextField(
        max_length=1024,
        unique=True,
    )  # 1024 is an arbitrary number

    # comment = models.CharField()
