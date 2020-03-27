from django.urls import path

from . import views

urlpatterns = [
    path('', views.directories, name='index'),
    path('directories', views.directories, name='index'),
    path('history', views.history, name='history'),
    path('history_single', views.history_single, name='history_single'),
    path('start_backup', views.start_backup, name='start_backup'),
    path('add_directory', views.add_directory, name='add_directory'),
    path('delete_directory', views.delete_directory, name='delete_directory'),
    path('delete_history', views.delete_history, name='delete_history'),
    path('download_backup', views.download_backup, name='download_backup'),
]
