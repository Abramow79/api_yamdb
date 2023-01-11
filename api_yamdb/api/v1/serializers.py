from reviews.models import Category, Title, Genre
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["id"]
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        default=None,
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def to_representation(self, instance):
        data = super(TitleSerializer, self).to_representation(instance)
        data['category'] = CategoriesSerializer(instance.category).data
        data['genre'] = GenresSerializer(instance.genre.all(), many=True).data
        return data


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["id"]
        model = Genre
