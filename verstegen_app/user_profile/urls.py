from django.urls import path
from . import views

urlpatterns = [
    path('user_admin/', views.user_manager, name='user_admin'),
    path('delete_user/<int:user_id>', views.user_delete, name='delete_user'),
]