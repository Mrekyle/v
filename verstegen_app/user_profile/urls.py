from django.urls import path
from . import views

urlpatterns = [
    path('user_admin/', views.user_manager, name='user_admin'),
    path('edit_user_modal/<int:user_id>/', views.user_edit_modal, name='edit_user_modal'),
    path('edit_user/<int:user_id>', views.user_profile_admin, name='edit_user'),
    path('delete_user_modal/<int:user_id>/', views.delete_user_modal, name='delete_user_modal'),
    path('delete_user/<int:user_id>', views.user_delete, name='delete_user'),
]