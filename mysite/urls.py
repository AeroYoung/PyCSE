from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('rapid', TemplateView.as_view(template_name='Rapid/index.html'), name='rapid'),
    path('', include('civil.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]

admin.site.site_header = '主页'
