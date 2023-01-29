from rest_framework import permissions
from users.models import UserRole


class Everyone(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.USER)
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.USER
                    and user == obj.author)
        return (request.method in permissions.SAFE_METHODS)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.MODERATOR)
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.MODERATOR)
        return False


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.ADMIN
                    or user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return (user.role == UserRole.ADMIN
                    or user.is_superuser)
        return False
