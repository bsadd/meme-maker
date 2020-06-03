from functools import wraps
from django.core.exceptions import PermissionDenied


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return wrapper


def moderator_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_moderator or request.user.is_superuser):
            return view(request, *args, **kwargs)
        raise PermissionDenied

    return wrapper


from rest_framework import exceptions


def api_auth_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        raise PermissionDenied

    return wrapper


def route_permissions(permission):
    """ django-rest-framework permission decorator for custom methods """

    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            if self.request.user.has_perm(permission):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()

        return _decorator

    return decorator
