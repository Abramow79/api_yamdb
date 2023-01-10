from django.shortcuts import get_object_or_404
from rest_framework import permissions
from users.models import User


class IsAdminmOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_staff or request.user.role == "admin"))


class IsAdminmMderator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(User, username=request.user.username)
        return user.role == "admin" or user.role == "moderator"


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы.
    Права на запросы для админа, аутентифицированного пользователя"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrModeRatOrOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):
    """
    Предоставляет права на осуществление запросов админу Джанго,
    модератору или аутентифицированному пользователю c ролью admin.
    Для неаутентифицированных пользователей доступны безопасные методы.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только админу Джанго или аутентифицированному пользователю c ролью admin.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только суперпользователю Джанго, админу Джанго или
    аутентифицированному пользователю c ролью admin.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin)
        )
