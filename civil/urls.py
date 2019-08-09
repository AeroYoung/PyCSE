from django.urls import path
from . import views

app_name = 'civil'
urlpatterns = [
    path('', views.index, name='index'),
]