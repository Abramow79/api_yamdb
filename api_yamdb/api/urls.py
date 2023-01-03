from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from .views import CategorieViewSet, GenreViwSet, TitlesViewSet
from .views import categorie_delete

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategorieViewSet, basename='categorie')
v1_router.register('genres', GenreViwSet, basename='genre')
v1_router.register('titles', TitlesViewSet, basename='title')

urlpatterns = [
    path('v1/categories/<slug:slug>/', categorie_delete),
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
