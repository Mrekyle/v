from django.db import models
from django.contrib.auth.models import AbstractUser as Base_User

class User(Base_User):
    """"
        Custom User Model

        Creating the base user group levels for the application.
         
        Allowing different roles to be assigned
    """
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=50, unique=True)
    fname = models.TextField(max_length=50, blank=True, null=True)

    ADMIN = 1
    STAFF = 2
    BUTCHER = 3
    USER = 4
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (BUTCHER, 'Butcher'),
        (USER, 'User'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'password', 'fname',]

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """
        Base user profile model

        Creating the base user profile for the application.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=10, choices=User.ROLE_CHOICES, default='User')
    date_joined = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    bio = models.TextField(null=True, blank=True, max_length=1024)
    butchery = models.CharField(max_length=100, null=True, blank=True)

    profile_img = models.ImageField(blank=True, null=True)
    profile_img_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.role
    