from django.db import models


class ModelWithTimestamps(models.Model):
    """Abstract base class for models that require timespamps of creation and modification"""

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
