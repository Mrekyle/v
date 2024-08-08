from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check if a user belongs to a specific group.
    """
    group = Group.objects.filter(name=group_name).first()
    return True if group and group in user.groups.all() else False