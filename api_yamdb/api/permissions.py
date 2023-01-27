from rest_framework import permissions


class Titles(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'user'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'moderator'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            return (user.role == 'user' and request.user == obj.author
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)


class Categories(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'user'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'moderator'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            return (request.method not in permissions.SAFE_METHODS
                    and (user.role == 'user'
                         and request.user == obj.author
                         or user.role == 'moderator'
                         and request.user == obj.author
                         or user.role == 'admin'
                         or user.is_superuser))
        except AttributeError:
            return False


class Genres(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'user'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'moderator'
                    and request.method in permissions.SAFE_METHODS
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            return (request.method not in permissions.SAFE_METHODS
                    and (user.role == 'user'
                         and request.user == obj.author
                         or user.role == 'moderator'
                         and request.user == obj.author
                         or user.role == 'admin'
                         or user.is_superuser))
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)


class Reviews(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'user'
                    or user.role == 'moderator'
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            return (request.user.role == 'user' and request.user == obj.author
                    or user.role == 'moderator'
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)


class Comments(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'user'
                    or user.role == 'moderator'
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            return (request.user.role == 'user' and request.user == obj.author
                    or user.role == 'moderator'
                    or user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return (request.method in permissions.SAFE_METHODS)


class Users(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return (user.role == 'admin'
                    or user.is_superuser)
        except AttributeError:
            return False
