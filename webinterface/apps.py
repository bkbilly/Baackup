from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from . import tasks


class WebinterfaceConfig(AppConfig):
    name = 'webinterface'
    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(tasks.update_forecast, 'interval', seconds=5)
        scheduler.start()
        print('----- started tasks')