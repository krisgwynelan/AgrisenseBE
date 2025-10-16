# agrusense>simulate_data.py
import os, django, time, random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")
django.setup()

channel_layer = get_channel_layer()

def send_random_data():
    data = {
        "temperature": round(random.uniform(20, 35), 2),
        "ph": round(random.uniform(5.5, 7.5), 2),
        "nitrogen": round(random.uniform(10, 50), 2),
        "phosphorus": round(random.uniform(5, 25), 2),
        "potassium": round(random.uniform(80, 250), 2),
    }
    async_to_sync(channel_layer.group_send)(
        "soil_data",
        {"type": "soil_update", "data": data}
    )
    print("Sent:", data)

while True:
    send_random_data()
    time.sleep(5)
