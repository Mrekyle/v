from django.shortcuts import render, redirect

from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, admin_only, allowed_users
from .models import User
from .forms import CreateCustomUser

# Create your views here.

@login_required(login_url='landing')
def user_admin(request):
    """
        Creates the admin user of the application
    """

    form = CreateCustomUser()

    role_selection = request.POST.get('id_role')

    # Check the role integer value 1, 2, 3, 4 to process the groups of the user

    if request.method == 'POST':
        print(role_selection)
        form = CreateCustomUser(request.POST)
        if form.is_valid():
            print(form.data)
            admin = form.save(commit=False)
            admin.role = User.ADMIN
            admin.is_active = True
            admin.save()
            group = Group.objects.get(name='Admin')
            group.user_set.add(admin)
            messages.success(request, f'New Admin user successfully registered')
            return redirect('user_admin')
            
    template = 'user-admin.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

# def register_user(request):
    """
        Creates the user user of the application
    """

    form = UserCreationForm()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.USER
            user.is_active = True
            user.save()
            group = Group.objects.get(name='User')
            group.user_set.add(user)
            messages.success(request, f'New User successfully registered')
            return redirect('home')
        

    template = 'user-control.html'
    context = {
        'form': form,
    }

    return redirect(request, template, context)