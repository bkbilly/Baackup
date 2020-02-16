from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
# from .tasks import TasksClass


class WebinterfaceConfig(AppConfig):
    name = 'webinterface'

    def ready(self):
        # tc = TasksClass(0)
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(tc.update_forecast, 'interval', seconds=5)
        # scheduler.start()
        print('----- started tasks')
