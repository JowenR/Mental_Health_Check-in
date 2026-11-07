from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def student_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_home")
        return view(request, *args, **kwargs)
    return wrapper


def admin_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("home")
        return view(request, *args, **kwargs)
    return wrapper