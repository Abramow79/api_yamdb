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
