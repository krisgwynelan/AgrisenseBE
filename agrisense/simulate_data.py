import os
import sys
import django
import asyncio
import random
from channels.layers import get_channel_layer

# Add your project directory to the Python path
sys.path.append("C:/Users/krist/agrisense")  # Update to your actual project path

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")

# Setup Django
django.setup()

# Async function to simulate and send dummy soil data
async def send_dummy_data():
    channel_layer = get_channel_layer()
    print("✅ Starting soil data simulation...")

    while True:
        data = {
            "temperature": round(random.uniform(25.0, 35.0), 2),
            "ph": round(random.uniform(5.5, 7.5), 2),
            "nitrogen": random.randint(10, 50),
            "phosphorus": random.randint(10, 50),
            "potassium": random.randint(10, 50),
        }

        # Send data to the group
        await channel_layer.group_send(
            "soil_data",
            {
                "type": "send_sensor_data",
                "data": data,
            }
        )

        # Print to console so you can see the result
        print("📡 Sending soil data:", data)

        # Wait for 3 seconds before sending again
        await asyncio.sleep(3)

# Run the async loop
if __name__ == "__main__":
    try:
        asyncio.run(send_dummy_data())
    except KeyboardInterrupt:
        print("\n❌ Simulation stopped by user.")
