# agrisense/celery.py
from celery import Celery
import os
from celery.schedules import crontab 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")

app = Celery("agrisense")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    "send-notification-every-midnight": {
        "task": "accounts.tasks.send_daily_summary",
        "schedule": crontab(minute=0, hour=0), # <-- runs exactly at 12:00 AM
    },
}

#