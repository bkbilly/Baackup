from django.urls import path

from . import views

urlpatterns = [
    path('', views.directories, name='index'),
    path('directories', views.directories, name='index'),
    path('history', views.history, name='history'),
    path('settings', views.settings, name='settings'),
]
