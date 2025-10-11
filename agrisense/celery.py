import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")

app = Celery("agrisense")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Schedule the daily summary (runs every 24h)
app.conf.beat_schedule = {
    "send-daily-soil-summary": {
        "task": "accounts.tasks.generate_daily_summary",
        "schedule": crontab(hour=20, minute=0),  # every 8PM
    },
}
