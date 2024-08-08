from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages



def unauthenticated_user(view_func):
    """
        Checks is a user is authenticated
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            messages.info(request, f'Please login to use the Verstegen.app')
            return view_func(request, *args, **kwargs)
        
    return wrapper_func


from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    """
    Checks the user's role and grants access to certain parts of the app based on the user's group.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Change to a new page redirection 
                return HttpResponse("Oops... It appears you are unable to access this page")
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
            messages.error(request, 'You do not have permission to view this page')
            return redirect('butcher')
        elif group == 'staff':
            messages.error(request, 'You do not have permission to view this page')
            return redirect('staff')
        elif group == 'user':
            messages.error(request, 'You do not have permission to view this page')
            return redirect('user')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_func