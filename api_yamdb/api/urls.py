from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from .views import CategorieViewSet, GenreViwSet, TitlesViewSet
from .views import categorie_delete, genres_delete

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategorieViewSet, basename='categories')
v1_router.register('genres', GenreViwSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/categories/<slug:slug>/', categorie_delete),
    path('v1/genres/<slug:slug>/', genres_delete),
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]

# from django.urls import include, path
# <<<<<<< HEAD
# from rest_framework.routers import DefaultRouter

# from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                     ReviewViewSet, TitleViewSet,
#                     UserViewSet)

# app_name = "api"

# v1_router = DefaultRouter()

# v1_router.register("users", UserViewSet, basename="users")
# v1_router.register("categories", CategoryViewSet, basename="categorie")
# v1_router.register("genres", GenreViewSet, basename="genre")
# v1_router.register("titles", TitleViewSet, basename="title")
# v1_router.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet, basename="comments"
# )
# v1_router.register(r"titles/(?P<title_id>\d+)/reviews",
#                    ReviewViewSet, basename="reviews")

# urlpatterns = [
#     path("v1/", include(v1_router.urls)),
#     path("v1/auth/", include("users.urls")),
