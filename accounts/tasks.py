# accounts/tasks.py
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime

@shared_task
def send_daily_summary():
    channel_layer = get_channel_layer()
    summary_payload = {
        "npk": {"N": 45, "P": 28, "K": 35},
        "ph": 6.8,
        "temperature": 30.5,
        "note": "Soil conditions stable 🌱"
    }

    async_to_sync(channel_layer.group_send)(
        "soil_data",
        {
            "type": "daily_summary",
            "title": "🌙 Daily Soil Summary",
            "message": f"Generated at {datetime.utcnow().isoformat()}",
            "summary": summary_payload,
        }
    )
