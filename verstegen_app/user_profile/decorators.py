from django.http import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_func):
    """
        Checks is a user is authenticated
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func


def allowed_users(allowed_roles=[]):
    """
        Checks the users role on the app and grants access to certain parts dependent on the user group
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.group.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Change to a new page redirection 
                return HttpResponse(f"Oops... It appears you are unable to access this page")
        return wrapper_func
    return decorator


def admin_only(view_func):
    """
        Checking if the users group is admin and directly accordingly
    """
    def wrapper_func(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.group.all()[0].name

        if group == 'butcher':
            return redirect('butcher')
        elif group == 'moderator':
            return redirect('moderator')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_func