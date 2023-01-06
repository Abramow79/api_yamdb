from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrModeRatOrOrAdminOrReadOnly,
                          IsSuperUserOrIsAdminOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitlePostSerialzier,
                          TitleSerializer, TokenRegSerializer,
                          UserSerializer)


from reviews.models import Category, Genre, Review, Title
from users.models import User


class AdminViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class SignUpApiView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response('Это имя или email уже существует',
                            status.HTTP_400_BAD_REQUEST)
        code = default_token_generator.make_token(user)
        send_mail(
            'Код токена',
            f'Код для получения токена {code}',
            settings.DEFAULT_FROM_EMAIL,
            [serializer.validated_data.get('email')]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenRegApiView(APIView):
    def post(self, request):
        serializer = TokenRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = (
                'Вы использовали неверный код подтверждения.')
            return Response({message}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdmin,)
#     filter_backends = (filters.SearchFilter,)
#     lookup_field = 'username'

#     @action(
#         methods=['patch', 'get'],
#         detail=False,
#         permission_classes=(IsAuthenticated,),
#     )
#     def me(self, request):
#         user = get_object_or_404(User, username=self.request.user)
#         serializer = UserEditSerializer(user)
#         if request.method == 'PATCH':
#             serializer = UserEditSerializer(
#                 user, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        """
        Обеспечивает получение и управление данными пользователя по username.
        """
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        """Позволяет пользователю получить и редактировать свою информацию."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            # serializer.save()
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(AdminViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdminViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerialzier
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
