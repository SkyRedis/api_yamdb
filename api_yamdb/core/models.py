from django.db import models

from reviews.models import Category, Genre


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет name."""
    name = models.CharField(
        max_length=256,
    )

    class Meta:
        abstract = True

    def fields_slug(slug):
        slug = models.SlugField(unique=True, max_length=50)
        if Category or Genre:
            return slug
        return None
