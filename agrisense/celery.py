# agrisense/celery.py
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")

app = Celery("agrisense")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# ✅ Use correct function name from accounts/tasks.py
# agrisense/celery.py
app.conf.beat_schedule = {
    "send-daily-soil-summary": {
        "task": "accounts.tasks.send_daily_summary",
        "schedule": crontab(hour=23, minute=59),  # 11:59 PM daily
    },
}

