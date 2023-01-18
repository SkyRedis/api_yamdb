from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.PositiveSmallIntegerField(
        choices=USER_ROLES,
        blank=True,
        default=1
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title_id = models.IntegerField(
        verbose_name='ID произведения',
    )
    # Заменить IntegerField на ForeignKey после создания модели произведений
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )

    def __str__(self) -> str:
        return f'{self.text[:15]}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_reviews'
            )
        ]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор коммента',
    )
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='ID отзыва',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации комментария',
    )

    def __str__(self) -> str:
        return f'{self.text[:15]}'

    class Meta():
        ordering = ['-pub_date']
