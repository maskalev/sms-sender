import logging
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbrq_api.settings")
logger = logging.getLogger("api")

app = Celery("fbrq_api", broker="amqp://guest:guest@rabbitmq:5672/")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "send_daily_statistics_email": {
        "task": "Statictics Email",
        "schedule": crontab(hour=0, minute=1),
    },
}
