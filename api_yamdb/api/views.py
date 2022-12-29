from reviews.models import Categories, Title, Genres
from rest_framework import viewsets
from .serializers import (CategoriesSerializer, TitleSerializer,
                          GenresSerializer)


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViwSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
