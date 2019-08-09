from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('<str:username>/edit_user/', views.edit, name='edit_user'),
]
