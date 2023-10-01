from django.db import models

from encrypted_model_fields import fields


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
    """Human readable name"""
    name = models.CharField(100)

    private_key_content = fields.EncryptedTextField(db_index=False)

    """ssh-key file content (That COULD be stripped of the comment at the end)"""
    public_key_content = models.TextField(db_index=False)  # 1024 is an arbitrary number

    # comment = models.CharField()
