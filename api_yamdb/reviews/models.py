from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

LENGTH_TEXT = 15

# Вставил классы Дмитрия, для оптимизации


class Genres(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(unique=True)


class Categories(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True,)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True)


# Нужна модель/класс, которая свяжет жанры и произведения


class Review(models.Model):
    """Класс отзывов."""

    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:LENGTH_TEXT]


class Comment(models.Model):
    """Класс комментариев."""

    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LENGTH_TEXT]
