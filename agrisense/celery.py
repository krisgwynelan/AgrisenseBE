# agrisense/celery.py
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")

app = Celery("agrisense")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# agrisense/celery.py
app.conf.beat_schedule = {
    "send-test-soil-summary": {
        "task": "accounts.tasks.send_daily_summary",
        "schedule": 20.0,  # every 20 seconds
    },
}

