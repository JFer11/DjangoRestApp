from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_function(request, *args, **kwargs)
        else:
            redirect('example')
    return wrapper_function


def allowed_users(allowed_groups=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_groups:
                        return view_function(request, *args, **kwargs)
            else:
                return redirect('bad_groups')
        return wrapper_function
    return decorator
