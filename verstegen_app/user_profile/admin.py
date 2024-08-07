from django.contrib import admin
from .models import User, UserProfile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    """
        Admin panel for the User Model        
    """

    list_display = ('email', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('email', 'username',)


class UserProfileAdmin(admin.ModelAdmin):
    """
        Admin panel for the UserProfile Model
    """

    list_display = ('user', 'butchery')
    list_filter = ('user', 'butchery')
    search_fields = ('user', 'butchery')


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)