from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title_id = models.IntegerField()
    # Заменить IntegerField на ForeignKey после создания модели произведений
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    pub_date = pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('author', 'title_id')


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    pub_date = pub_date = models.DateTimeField(
        auto_now_add=True,
    )
