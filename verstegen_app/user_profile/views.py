from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, admin_only, allowed_users
from .models import User
from .forms import CreateCustomUser, UserProfileForm

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

    roles = {
        '1': {'role': User.ADMIN, 'group': 'Admin'},
        '2': {'role': User.STAFF, 'group': 'Staff'},
        '3': {'role': User.BUTCHER, 'group': 'Butcher'},
        '4': {'role': User.USER, 'group': 'User'},
    }

    if request.method == 'POST':
        form = CreateCustomUser(request.POST)
        if role_selection in roles:
            role_data = roles[role_selection] 
            if form.is_valid():
                user = form.save(commit=False)
                user.role = role_data['role'] 
                user.is_active = True
                user.save()
                group = Group.objects.get(name=role_data['group'])
                group.user_set.add(user)
                messages.success(request, f'New {role_data["group"]} {username}: Was successfully registered')
                return redirect('user_admin')
            else:
                messages.error(request, f'Please check the form and try again.')
        else:
            messages.error(request, f'Oops.. Something went wrong, Please take another look \
                           and try again.')       
            
    template = 'user-admin.html'
    context = {
        'form': form,
        'users': users,
        'count': user_count,
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

# def edit_user(request, user_id):
#     user = User.objects.get(pk=user_id)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile', pk=user_id)
#     else:
#         form = UserProfileForm(instance=user)
#     return render(request, 'edit_user_profile.html', {'form': form})

@login_required(login_url='landing')
def user_edit(request, user_id):
    """
    Allows the Staff to edit the users 
    """

    user = get_object_or_404(User, id=user_id)
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} was successfully updated')
            return redirect('user_admin')
        else:
            messages.error(request, f'Something went wrong. Please check the form and try again.')
    else:
        form = UserProfileForm(instance=user)
        messages.info(request, f'You are currently editing user profile: {user.username}')

    template = 'user-admin.html'
    context = {
        'edit_form': form,
        'user': user,
    }
    return render(request, template, context)