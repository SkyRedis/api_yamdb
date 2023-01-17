from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


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
        return self.text

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
        return self.text

    class Meta():
        ordering = ['-pub_date']


class Categories(models.Model):
    name = models.CharField(
        'categories_name',
        max_length=256,
    )
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(
        'genres_name',
        max_length=256,
    )
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Titles(models.Model):
    # Возможно нужно добавить author и rating
    name = models.CharField(
        'titles_name',
        max_length=256,
    )
    year = models.IntegerField()
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitles'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-year']


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.titles}'
