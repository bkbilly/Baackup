# Generated by Django 3.0.3 on 2020-02-15 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0004_logs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directories',
            name='exclude_dirs',
        ),
        migrations.AddField(
            model_name='directories',
            name='exclude_dirs',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
        migrations.DeleteModel(
            name='ExcludedDirs',
        ),
    ]
