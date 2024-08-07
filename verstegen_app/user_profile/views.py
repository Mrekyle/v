from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, admin_only, allowed_users
from .models import User
from .forms import CreateCustomUser

# Create your views here.

@login_required(login_url='landing')
def user_manager(request):
    """
        Creates the admin user of the application
    """

    users = User.objects.all()
    user_count = users.count()
    form = CreateCustomUser()

    role_selection = request.POST.get('role')
    username = request.POST.get(str('username'))

    """
        Manual user registration
    """
    if request.method == 'POST':
        form = CreateCustomUser(request.POST)
        if role_selection == '1':
            if form.is_valid():
                admin = form.save(commit=False)
                admin.role = User.ADMIN
                admin.is_active = True
                admin.save()
                group = Group.objects.get(name='Admin')
                group.user_set.add(admin)
                messages.success(request, f'New {role_selection} {username}: Was successfully registered')
                return redirect('user_admin')
            else:
                messages.error(request, f'Please check the form and try again.')
        elif role_selection == '2':
            if form.is_valid():
                staff = form.save(commit=False)
                staff.role = User.STAFF
                staff.is_active = True
                staff.save()
                group = Group.objects.get(name='Staff')
                group.user_set.add(staff)
                messages.success(request, f'New {role_selection} {username}: Was successfully registered')
                return redirect('user_admin')
            else:
                messages.error(request, f'Please check the form and try again.')
        elif role_selection == '3':
            if form.is_valid():
                butcher = form.save(commit=False)
                butcher.role = User.BUTCHER
                butcher.is_active = True
                butcher.save()
                group = Group.objects.get(name='Butcher')
                group.user_set.add(butcher)
                messages.success(request, f'New {role_selection} {username}: Was successfully registered')
                return redirect('user_admin')
            else:
                messages.error(request, f'Please check the form and try again.')
        elif role_selection == '4':
            if form.is_valid():
                user = form.save(commit=False)
                user.role = User.USER
                user.is_active = True
                user.save()
                group = Group.objects.get(name='User')
                group.user_set.add(user)
                messages.success(request, f'New {role_selection} {username}: Was successfully registered')
                return redirect('user_admin')
            else:
                messages.error(request, f'Please check the form and try again.')    
        else:
            messages.error(request, f'Oops.. Something went wrong. Please take another look at the form \
                        and please try again.')
            
    template = 'user-admin.html'
    context = {
        'form': form,
        'users': users,
        'count': user_count,
    }

    return render(request, template, context)

@login_required(login_url='landing')
@allowed_users(allowed_roles=['Admin', 'Staff'])
def user_edit(request, pk):
    """
        Allows the Staff to edit the users 
    """

    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        form = CreateCustomUser(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, f'User {pk} was successfully updated')
            return redirect('user_admin')
        else:
            messages.error(request, f'Something went wrong. Please check the form and try again.')
    else:
        form = CreateCustomUser(instance=user)
        messages.info(request, f'You are currently editing user profile: {pk}')

    template = ''
    context = {
        'form': form,
        'user': user,
    }
    return render(request, template, context)

@login_required(login_url='landing')

def user_delete(request, user_id):
    """
        Allows the Admin to delete the users
    """

    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, f'User {user.username} was successfully deleted')
    return redirect(reverse('user_admin'))