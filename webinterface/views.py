from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from .models import Directories, BackupHistory, Logs, DirectoriesStatus
# from django.template import loader
from .tasks import TasksClass
from .forms import AddDirectoryForm


import os
import zipfile
from io import BytesIO
import pyAesCrypt
import shutil


def make_zip(backup_path):
    s = BytesIO()
    zipf = zipfile.ZipFile(s, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return s.getvalue()


def encrypt(pbdata, password):
    bufferSize = 64 * 1024

    # input plaintext binary stream
    fIn = BytesIO(pbdata)
    # initialize ciphertext binary stream
    fCiph = BytesIO()
    # encrypt stream
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
    return fCiph.getvalue()


def decrypt(aes_file, password):
    bufferSize = 64 * 1024

    fCiph = BytesIO(aes_file)
    # get ciphertext length
    ctlen = len(aes_file)
    # go back to the start of the ciphertext stream
    fCiph.seek(0)
    # initialize decrypted binary stream
    fDec = BytesIO()
    # decrypt stream
    success = True
    try:
        pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
    except Exception as e:
        success = e
        print(e)

    return fDec.getvalue(), success


def create_backuphistory(file, size='', comment='', processed=[]):
    model_backup = BackupHistory(
        processed_date=datetime.now(),
        size=size,
        comment=comment,
        file=file)
    model_backup.save()
    for proc in processed:
        model_dir = DirectoriesStatus(
            name=proc['name'],
            size=proc['size'],
            exists=proc['exists']
        )
        model_dir.save()
        model_backup.directories_status.add(model_dir)
    model_backup.save()


@csrf_exempt
def start_backup(request):
    password = request.GET.get('password')
    dirpath = 'temp_baackup'
    tc = TasksClass(dirpath)
    location, size, processed = tc.backup()
    comment = ''
    didnotprocess = [sub['name']
                     for sub in processed if sub['exists'] is not True]
    if len(didnotprocess) > 0:
        comment = 'rejected: {}'.format(','.join(didnotprocess))

    myzip = make_zip(dirpath)
    aes_out = encrypt(myzip, password)
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    create_backuphistory(aes_out, size, comment, processed)

    return redirect('history')


def download_backup(request):
    item_id = request.GET.get('item_id')
    password = request.GET.get('password')
    history = BackupHistory.objects.get(id=item_id)
    zip_filename = 'baackup-{}.zip'.format(
        history.processed_date.strftime("%Y-%m-%d_%H-%M-%S")
    )

    zip_out, success = decrypt(history.file, password)

    if success is True:
        # Grab ZIP file from in-memory, make response with correct Content-type
        resp = HttpResponse(
            zip_out, content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        updateObject = BackupHistory.objects.filter(id=item_id)
        updateObject.update(comment='')

        return resp
    else:
        updateObject = BackupHistory.objects.filter(id=item_id)
        updateObject.update(comment=success)
        return HttpResponseRedirect('history')


def add_directory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddDirectoryForm(data=request.POST)
        # check whether it's valid:
        print(form.is_valid())
        if form.is_valid():
            form.cleaned_data['backup_type'] = 'folder'
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
                updateObject = Directories.objects.filter(
                    id=form.cleaned_data['edit_id'])
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


def delete_directory(request):
    item_id = request.GET.get('item_id')
    Directories.objects.filter(id=item_id).delete()

    return HttpResponseRedirect('directories')


def delete_history(request):
    item_id = request.GET.get('item_id')
    BackupHistory.objects.filter(id=item_id).delete()

    return HttpResponseRedirect('history')


def directories(request):
    directories = Directories.objects.order_by('name').all()
    context = {'tab': 'Directories', 'directories': directories}
    return render(request, 'webinterface/directories.html', context)


def history(request):
    history = BackupHistory.objects.order_by('-processed_date').all()
    context = {'tab': 'History', 'history': history}
    return render(request, 'webinterface/history.html', context)


def history_single(request):
    item_id = request.GET.get('item_id')
    history = BackupHistory.objects.get(id=item_id)
    directories = history.directories_status.all()
    context = {'tab': 'History', 'history': history,
               'directories': directories}
    return render(request, 'webinterface/history_single.html', context)
