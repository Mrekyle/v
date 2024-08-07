from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
        Signals function for creating the new user profile on the application
    """
    if created:
        UserProfile.objects.create(user=instance)
        print('New user account created.')
    else:
        try:
            """
                Creates the user profile
            """
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('User profile was created successfully.')
        except:
            """
                Creates the user profile if the user doesn't exist
            """
            UserProfile.objects.create(user=instance)
            print('User did\'nt exist. New user now created.')