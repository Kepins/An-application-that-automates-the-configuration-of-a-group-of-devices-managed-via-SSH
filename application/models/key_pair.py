from django.db import models


class KeyPair(models.Model):
    """ssh-key pair that has content of ssh-keygen generated files"""

    # class TypeOfKey(models.TextChoices):
    #     DSA = "dsa"
    #     ECDSA = "ecdsa"
    #     ECDSA_SK = "ecdsa-sk"
    #     ED25519 = "ed25519"
    #     ED25519_SK = "ed25519-sk"
    #     RSA = "rsa"

    # type = models.CharField(choices=TypeOfKey.choices)

    private_key_content = models.TextField(
        unique=True,
    )

    """ssh-key file content (That COULD be stripped of the comment at the end)"""
    public_key_content = models.TextField(
        unique=True,
    )  # 1024 is an arbitrary number

    # comment = models.CharField()
