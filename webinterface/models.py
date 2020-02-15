from django.db import models
import os.path

# Create your models here.


class Notification(models.Model):
    sender = models.CharField(max_length=200, default='')


class ExcludedDirs(models.Model):
    directory = models.CharField(max_length=200, default='')


class Directories(models.Model):
    date_added = models.DateTimeField('date added')
    name = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=50, default='local')
    backup_type = models.CharField(max_length=50, default='folder')
    path = models.CharField(max_length=200, default='')
    remote_url = models.CharField(max_length=200, default='', blank=True)
    remote_user = models.CharField(max_length=100, default='', blank=True)
    remote_pass = models.CharField(max_length=100, default='', blank=True)
    exclude_dirs = models.ManyToManyField(ExcludedDirs, blank=True)

    def summary_path(self):
        sumpath = self.path
        if self.location not in ['local', '']:
            sumpath = '{}@{}:{}'.format(
                self.remote_user,
                self.remote_url,
                self.path)
        return sumpath


class Settings(models.Model):
    run_hour = models.IntegerField(default=4)
    tmp_dir = models.CharField(max_length=200, default='./')
    encrypt_pass = models.CharField(max_length=100, default='1234')
    notification = models.ManyToManyField(Notification)


class BackupHistory(models.Model):
    processed_date = models.DateTimeField('Created date')
    path = models.CharField(max_length=200, default='')
    size = models.CharField(max_length=50, default='')

    def exists(self):
        exists = False
        if os.path.isfile(self.path):
            exists = True
        return exists
    # exists = models.BooleanField(default=True)


class Logs(models.Model):
    date = models.DateTimeField('Date')
    message = models.CharField(max_length=1000, default='')
