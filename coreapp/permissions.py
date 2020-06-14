from rest_framework import permissions


class IsModerator(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
                request.user.is_moderator or request.user.is_superuser) and not request.user.is_suspended
