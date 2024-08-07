from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from user_profile.decorators import unauthenticated_user, admin_only, allowed_users


# Create your views here.
@login_required(login_url='landing')
def home(request):
    """
        Home of the application
    """

    template = 'index.html'
    context = {
        'home': True,
    }

    return render(request, template, context)