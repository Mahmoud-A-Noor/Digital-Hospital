from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


def user_type_required(user_type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            return render(request, 'dashboard/403_error.html', status=403)
        return wrapper
    return decorator

