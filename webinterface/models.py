from django.db import models

# Create your models here.
class Notification(models.Model):
	sender = models.CharField(max_length=200)

class ExcludedDirs(models.Model):
	directory = models.CharField(max_length=200)

class Directories(models.Model):
    date_added = models.DateTimeField('date added')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=50)
    backup_location = models.CharField(max_length=50)
    remote_url = models.CharField(max_length=200)
    remote_user = models.CharField(max_length=200)
    remote_pass = models.CharField(max_length=200)
    exclude_dirs = models.ManyToManyField(ExcludedDirs)

class Settings(models.Model):
    run_hour = models.IntegerField(default=4)
    tmp_dir = models.CharField(max_length=200)
    encrypt_pass = models.CharField(max_length=100)
    notification = models.ManyToManyField(Notification)
