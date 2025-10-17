# accounts/tasks.py
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

async def send_to_user(user, summary_payload, today_str):
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"
    await channel_layer.group_send(
        group_name,
        {
            "type": "daily_summary",
            "title": "🌙 Daily Soil Summary",
            "message": f"Summary for {today_str}",
            "summary": summary_payload,
            "date": today_str,
        }
    )

@shared_task
def send_daily_summary():
    summary_payload = {
        "npk": {"N": 45, "P": 28, "K": 35},
        "ph": 6.8,
        "temperature": 30.5,
        "note": "Soil conditions stable 🌱"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    for user in User.objects.all():
        async_to_sync(send_to_user)(user, summary_payload, today_str)
        print(f"📩 Sent summary to {user.username}")