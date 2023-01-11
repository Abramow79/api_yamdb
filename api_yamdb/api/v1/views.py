
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from reviews.models import Category, Title, Genre
from rest_framework import filters, viewsets
from .serializers import (CategoriesSerializer, TitleSerializer,
                          GenresSerializer)
from .permissions import (IsAdminmOrReadOnly)
from .filters import TitleFilter


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminmOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


@api_view(['DELETE'])
@permission_classes([IsAdminmOrReadOnly])
def categorie_delete(request, slug):
    categorie = Category.objects.get(slug=slug)
    if request.method == 'DELETE':
        categorie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViwSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminmOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


@api_view(['DELETE'])
@permission_classes([IsAdminmOrReadOnly])
def genres_delete(request, slug):
    genres = Genre.objects.get(slug=slug)
    if request.method == 'DELETE':
        genres.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminmOrReadOnly, )
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)
