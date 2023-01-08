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
