from django.db import models


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
