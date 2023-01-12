from django.urls import include, path
from rest_framework import routers
from .views import SignUpApiView, TokenRegApiView

from .views import (CategorieViewSet, CommentViewSet, GenreViwSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet,
                    categorie_delete, genres_delete)

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategorieViewSet, basename='categories')
router.register('genres', GenreViwSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register("users", UserViewSet, basename="users")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet, basename="comments")
router.register(r"titles/(?P<title_id>\d+)/reviews",
                ReviewViewSet, basename="reviews")

urlpatterns = [
    # path('v1/categories/<slug:slug>/', categorie_delete),
    # path('v1/genres/<slug:slug>/', genres_delete),
    # path("v1/", include(v1_router.urls)),
    # path("v1/auth/", include("users.urls")),
    path('categories/<slug:slug>/', categorie_delete),
    path('genres/<slug:slug>/', genres_delete),
    path("", include(router.urls)),
    # path("auth/", include("users.urls")),
    path("auth/signup/", SignUpApiView.as_view(), name="signup"),
    path("auth/token/", TokenRegApiView.as_view(), name="token_access"),
]
