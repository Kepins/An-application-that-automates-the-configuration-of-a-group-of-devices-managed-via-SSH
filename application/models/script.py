from django.db import models


class Script(models.Model):

    """Human readable name"""

    name = models.CharField(max_length=100)

    """The content of script"""
    script = models.TextField()

    def __str__(self):
        return self.name
