from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from accounts.models import SensorReading  # ✅ your sensor model

User = get_user_model()

@shared_task
def send_daily_summary():
    """
    Send a WebSocket notification to all users using the latest soil sensor data.
    """
    print("📤 Celery task running... Fetching latest soil data from SensorReading")

    timestamp = datetime.now()
    channel_layer = get_channel_layer()

    # ✅ Get most recent reading
    latest_reading = SensorReading.objects.filter(
        timestamp__gte=timestamp - timedelta(minutes=1)
    ).order_by("-timestamp").first()

    if not latest_reading:
        print("⚠️ No recent sensor data found in the last 1 minute.")
        return

    # ✅ Prepare clean data payload
    data = {
        "temperature": latest_reading.temperature,
        "ph": latest_reading.ph,
        "nitrogen": latest_reading.nitrogen,
        "phosphorus": latest_reading.phosphorus,
        "potassium": latest_reading.potassium,
    }

    print(f"🌱 Using latest reading: {data}")

    # ✅ Send notification to all users
    for user in User.objects.all():
        group_name = f"user_{user.id}"

        message_data = {
            "title": "🌿 Real-Time Soil Update",
            "message": f"Hi {user.username}, here’s your latest soil summary (recorded at {latest_reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')})",
            "date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # ✅ ensure date included
            "summary": {
                "note": "Auto-generated from the most recent simulated data 🌾",
                **data,
            },
        }

        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "send_notification",
                    "message": message_data,
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            print(f"📩 Sent to {user.username}: {data}")

        except Exception as e:
            print(f"⚠️ Failed to send to {user.username}: {e}")

    print("✅ Celery broadcast complete.")
