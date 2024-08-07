from typing import Any
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User

class CreateCustomUser(UserCreationForm):
    """
        Creates a custom form for user creation
    """

    group_choices = {
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('butcher', 'Butcher'),
        ('user', 'User'),
    }

    username = forms.CharField(label='Username', min_length=2, max_length=150)
    email = forms.EmailField(label='Email')
    password0 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    role = forms.Select(choices=group_choices)

    widgets = {
        'role': forms.Select(choices=group_choices, attrs={
            'class': 'form-select',
            'id': 'id_role',
            'required': 'required',})
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password0', 'password1', 'role', ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email is already registered to an account.")
        return email
        
    def clean_password2(self):
        password0 = self.cleaned_data.get('password1')
        password1 = self.cleaned_data.get('password2')
        if password0 and password1 and password0 != password1:
            raise ValidationError("Passwords don't match")
        return password1

    def clean_group(self):
        group = self.cleaned_data.get('group')
        new = User.objects.filter(group=group)
        if new.count():
            raise ValidationError("Group doesn\'t exist.")
        return group
    

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            role=self.cleaned_data['role']
        )
        return user