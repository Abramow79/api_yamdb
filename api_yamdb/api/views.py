from reviews.models import Categories, Title, Genres
from rest_framework import viewsets
from .serializers import (CategoriesSerializer, TitleSerializer,
                          GenresSerializer)
from .permissions import IsAuthorOrReadOnly


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class GenreViwSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)
