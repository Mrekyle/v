from django.urls import path
from . import views

urlpatterns = [
    path('user_admin/', views.user_admin, name='user_admin'),
]