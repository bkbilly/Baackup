from django.contrib import admin

# Register your models here.
from .models import Directories, Settings, BackupHistory, Logs

admin.site.register(Directories)
admin.site.register(Settings)
admin.site.register(BackupHistory)
admin.site.register(Logs)
