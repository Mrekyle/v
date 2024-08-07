from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from user_profile.decorators import unauthenticated_user

from user_profile.models import User

# Create your views here.

@unauthenticated_user
def landing(request):
    """
        Landing page for the application

        Handling manual user authentication
    """

    form_button = request.POST.get('form_button')

    if request.method == 'POST':
        if form_button == 'register':
            user = User.objects.create_user(username=request.POST.get('username'), 
                            email=request.POST.get('email'), password=request.POST.get('password0'), role=User.USER)
            if request.status_code == 200:
                messages.success(request, f'New User successfully registered')
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, f'User registration failed, please try again')
        elif form_button == 'login':
            username = request.POST.get('username')
            email = request.POST.get('username')
            password = request.POST.get('password0')

            user = authenticate(request, username=('username'), password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, f'Username or password is incorrect, please try again')
        else:
            messages.info(request, f'Please select an option to continue using the application')

    template = 'landing.html'

    context = {
        'landing': True,
    }

    return render(request, template, context)

def logoutUser(request):
    """
        Manual logout logic handling
    """

    logout(request)
    return redirect('landing')