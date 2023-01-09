from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from reviews.utilites import current_year


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[MinValueValidator(
                    limit_value=settings.MIN_LIMIT_VALUE,
                    message="Год не может быть меньше или равен нулю"),
                    MaxValueValidator(
                    limit_value=current_year,
                    message="Год не может быть больше текущего")])
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(Genre,
                                   null=True,
                                   verbose_name='Жанры', related_name='genres')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='categories', blank=True,
                                 verbose_name='Категория',)

    class Meta:
        default_related_name = "titles"
