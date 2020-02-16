from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Directories, BackupHistory, Logs
# from django.template import loader
from .tasks import TasksClass
from .forms import AddDirectoryForm


def start_backup(request):
    tc = TasksClass()
    tc.backup()
    return redirect('history')


def add_directory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddDirectoryForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.cleaned_data['backup_type'] = 'folder'
            if form.cleaned_data['remote_url'] == '':
                form.cleaned_data['location'] = 'local'
            else:
                form.cleaned_data['location'] = 'remote'
            if form.cleaned_data['remote_port'] is None:
                form.cleaned_data['remote_port'] = 22
            excluded = form.cleaned_data['exclude_dirs']
            excluded = excluded.replace('\r', '').replace(' ', '')
            excluded = excluded.split('\n')
            excluded = ','.join(excluded)
            form.cleaned_data['exclude_dirs'] = excluded

            # Update database
            if form.cleaned_data['edit_id'] == 0:
                print(form.cleaned_data)
                newdir = Directories(
                    date_added=datetime.now(),
                    name=form.cleaned_data['name'],
                    location=form.cleaned_data['location'],
                    backup_type=form.cleaned_data['backup_type'],
                    path=form.cleaned_data['path'],
                    remote_url=form.cleaned_data['remote_url'],
                    remote_port=form.cleaned_data['remote_port'],
                    remote_user=form.cleaned_data['remote_user'],
                    remote_pass=form.cleaned_data['remote_pass'],
                    exclude_dirs=form.cleaned_data['exclude_dirs'])
                newdir.save()
            else:
                updateObject = Directories.objects.filter(id=form.cleaned_data['edit_id'])
                updateObject.update(
                    name=form.cleaned_data['name'],
                    location=form.cleaned_data['location'],
                    backup_type=form.cleaned_data['backup_type'],
                    path=form.cleaned_data['path'],
                    remote_url=form.cleaned_data['remote_url'],
                    remote_port=form.cleaned_data['remote_port'],
                    remote_user=form.cleaned_data['remote_user'],
                    remote_pass=form.cleaned_data['remote_pass'],
                    exclude_dirs=form.cleaned_data['exclude_dirs'])

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('directories')

    # if a GET (or any other method) we'll create a blank form
    else:
        item_id = request.GET.get('item_id')
        form = AddDirectoryForm(item_id=item_id)

    return render(request, 'webinterface/addDirectory.html', {'form': form})


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
