from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет name."""
    name = models.CharField(
        max_length=256,
    )

    class Meta:
        abstract = True
