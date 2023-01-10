from reviews.models import Category, Title, Genre
from rest_framework import serializers

import datetime as dt

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User
from users.validators import username_me


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


# import datetime as dt

# from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.shortcuts import get_object_or_404
# from rest_framework import serializers

# from reviews.models import Category, Comments, Genre, Review, Title
# from users.models import User
# from users.validators import username_me


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=settings.LIMIT_USERNAME,
                                      regex=r"^[\w.@+-]+\Z", required=True)
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True)

    def validate_username(self, value):
        return username_me(value)


class TokenRegSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=settings.LIMIT_USERNAME,
                                      regex=r"^[\w.@+-]+\Z", required=True)
    confirmation_code = serializers.CharField(max_length=settings.LIMIT_CHAT,
                                              required=True)

    def validate_username(self, value):
        return username_me(value)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")

    def validate_username(self, username):
        if username in "me":
            raise serializers.ValidationError(
                "Использовать имя me запрещено")
        return username


class UserEditSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


# class CategorySerializer(serializers.ModelSerializer):
#     """Сериализатор модели Category."""

#     class Meta:
#         model = Category
#         fields = ("name", "slug")


# class GenreSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Genre."""

#     class Meta:
#         model = Genre
#         fields = ("name", "slug")


# class TitleSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Title."""
#     genre = GenreSerializer(many=True)
#     category = CategorySerializer()
#     rating = serializers.IntegerField(default=1)

#     class Meta:
#         model = Title
#         fields = ("id", "name", "year", "rating",
#                   "description", "genre", "category",)
#         read_only_fields = ("id", "name", "year", 'rating',
#                             "description", "genre", "category",)


class TitlePostSerialzier(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ("id", "name", "year", 'rating',
                  "description", "genre", "category",)

    def validate_year(self, value):
        current_year = dt.date.today().year
        if (value > current_year):
            raise serializers.ValidationError(
                "Год произведения не может быть больше текущего."
            )
        return value

    def to_representation(self, instance):
        """Изменяет отображение информации в ответе (response)
         после POST запроса, в соответствии c техзаданием"""
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    score = serializers.IntegerField(validators=[
        MinValueValidator(limit_value=settings.MIN_LIMIT_VALUE,
                          message="Минимальное значение рейтинга - 1"),
        MaxValueValidator(limit_value=settings.MAX_LIMIT_VALUE,
                          message="Максимальное значение рейтинга - 10")
    ])

    def validate(self, data):
        if self.context.get("request").method == "POST":
            author = self.context.get("request").user
            title_id = self.context.get("view").kwargs.get("title_id")
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title_id=title.id,
                                     author=author).exists():
                raise ValidationError("Вы можете оставлять только один отзыв!")
        return data

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comments."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comments
        fields = ("id", "text", "pub_date", "author", "review")
        read_only_fields = ("review",)