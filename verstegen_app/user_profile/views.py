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
    new_user = CreateCustomUser()

    role_selection = request.POST.get('role')
    username = request.POST.get(str('username'))

    roles = {
        '1': {'role': User.ADMIN, 'group': 'Admin'},
        '2': {'role': User.STAFF, 'group': 'Staff'},
        '3': {'role': User.BUTCHER, 'group': 'Butcher'},
        '4': {'role': User.USER, 'group': 'User'},
    }


    """
        Manual User role selection
    """
    if request.method == 'POST':
        new_user = CreateCustomUser(request.POST)
        if role_selection in roles:
            role_data = roles[role_selection] 
            if new_user.is_valid():
                user = new_user.save(commit=False)
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
    else:
        new_user = CreateCustomUser()
            
    template = 'user-admin.html'
    context = {
        'new_user': new_user,
        'users': users,
        'count': user_count,
    }

    return render(request, template, context)


@login_required(login_url='landing')
@allowed_users(allowed_roles=['Admin'])
def user_profile_admin(request, user_id):
    """
    Allows the admin to pull up the suers information and edit the user
    """
    
    user = get_object_or_404(User, id=user_id)
    edit_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        edit_form = UserProfileForm(request.POST, instance=user)

        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'User {user.username} was successfully updated')
            return redirect('user_admin')
        else:
            messages.error(request, f'Something went wrong. Please check the form and try again.')
    else:
        edit_form = UserProfileForm(instance=user)
        messages.info(request, f'You are currently editing user profile: {user.username}')


    template = 'user_edit.html'
    context ={
        'edit_user': edit_form,
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

@login_required(login_url='landing')
def delete_user_modal(request, user_id):
    """
        User delete modal
    """
    user = User.objects.get(id=user_id)
    return render(request, 'delete_user_modal.html', {'user': user})

@login_required(login_url='landing')
def user_edit_modal(request, user_id):
    """
        User edit modal
    """
    user = User.objects.get(id=user_id)
    return render(request, 'edit_user_modal.html', {'user': user})