from rest_framework import permissions

from coreapp.constants import UPDATE_METHODS


class IsModerator(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
                request.user.is_moderator or request.user.is_superuser) and not request.user.is_suspended


class IsAuthenticatedCreateOrOwnerModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def __init__(self, owner_var_name='author'):
        self.owner_var_name = owner_var_name

    def has_object_permission(self, request, view, obj):
        return request.method not in UPDATE_METHODS or getattr(obj, self.owner_var_name, None) == request.user
