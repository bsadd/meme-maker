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
