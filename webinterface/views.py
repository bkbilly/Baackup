from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse
from .models import Directories, BackupHistory, Logs
# from django.template import loader
from .tasks import TasksClass


def start_backup(request):
    tc = TasksClass()
    tc.backup()
    return redirect('history')


def directories(request):
    directories = Directories.objects.order_by('name').all()
    context = {'tab': 'Directories', 'directories': directories}
    return render(request, 'webinterface/directories.html', context)


def history(request):
    history = BackupHistory.objects.order_by('-processed_date').all()
    context = {'tab': 'History', 'history': history}
    return render(request, 'webinterface/history.html', context)


def settings(request):
    logs = Logs.objects.order_by('date').all()
    context = {'tab': 'Settings', 'logs': logs}
    return render(request, 'webinterface/settings.html', context)
