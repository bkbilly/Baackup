from django.db import models
import os.path
from stat import S_ISDIR
import paramiko

# Create your models here.


class Notification(models.Model):
    sender = models.CharField(max_length=200, default='')


# class ExcludedDirs(models.Model):
#     directory = models.CharField(max_length=200, default='')


class Directories(models.Model):
    date_added = models.DateTimeField('date added')
    name = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=50, default='local')
    backup_type = models.CharField(max_length=50, default='folder')
    path = models.CharField(max_length=200, default='')
    remote_url = models.CharField(max_length=200, default='', blank=True)
    remote_user = models.CharField(max_length=100, default='', blank=True)
    remote_pass = models.CharField(max_length=100, default='', blank=True)
    exclude_dirs = models.CharField(max_length=5000, default='', blank=True)
    remote_port = models.IntegerField(default=22)
    # exclude_dirs = models.ManyToManyField(ExcludedDirs, blank=True)

    def summary_path(self):
        sumpath = self.path
        if self.location not in ['local', '']:
            sumpath = '{}@{}:{}'.format(
                self.remote_user,
                self.remote_url,
                self.path)
        return sumpath

    def exists(self):
        # print('---->', self.location, self.name, self.remote_url)
        exists = False
        if self.location in ['local', '']:
            if os.path.exists(self.path):
                exists = True
        elif self.location == 'remote':
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.remote_url,
                            username=self.remote_user,
                            password=self.remote_pass,
                            timeout=3)
                sftp = ssh.open_sftp()

                try:
                    sftp.stat(self.path)
                    exists = True
                except FileNotFoundError:
                    exists = False
            except Exception as e:
                print(e)
                exists = "Can't connect"
        return exists


class Settings(models.Model):
    run_hour = models.IntegerField(default=4)
    tmp_dir = models.CharField(max_length=200, default='./')
    encrypt_pass = models.CharField(max_length=100, default='1234')
    notification = models.ManyToManyField(Notification)


class BackupHistory(models.Model):
    processed_date = models.DateTimeField('Created date')
    path = models.CharField(max_length=200, default='')
    size = models.CharField(max_length=50, default='')
    comment = models.CharField(max_length=500, default='')

    def exists(self):
        exists = False
        if os.path.exists(self.path):
            exists = True
        return exists
    # exists = models.BooleanField(default=True)


class Logs(models.Model):
    date = models.DateTimeField('Date')
    message = models.CharField(max_length=1000, default='')
