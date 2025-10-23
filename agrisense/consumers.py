import json
import random
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer


class SoilConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user or user.is_anonymous:
            print("❌ Anonymous user tried to connect to Soil WebSocket")
            await self.close(code=403)
            return

        self.user = user
        self.group_name = f"user_{user.id}_soil"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ Soil WebSocket connected for user {user.username}")

        asyncio.create_task(self.send_fake_soil_data())

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"❌ Soil WebSocket disconnected for {getattr(self.user, 'username', 'unknown')}")

    async def soil_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "soil_update",
            "data": event["data"]
        }))

    async def send_fake_soil_data(self):
        try:
            while True:
                fake_data = {
                    "temperature": round(random.uniform(20, 35), 1),
                    "ph": round(random.uniform(5.5, 7.5), 2),
                    "nitrogen": round(random.uniform(15, 50), 1),
                    "phosphorus": round(random.uniform(10, 40), 1),
                    "potassium": round(random.uniform(80, 250), 1),
                }
                await self.send(json.dumps({
                    "type": "soil_update",
                    "data": fake_data
                }))
                await asyncio.sleep(10)
        except Exception as e:
            print(f"⚠️ Soil data loop stopped: {e}")


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
        else:
            self.user = user
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"✅ WS Connected for {user.username}")

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"❌ WS Disconnected for {getattr(self.scope['user'], 'username', 'unknown')}")

    async def send_notification(self, event):
        """
        Event sent by Celery to WebSocket group.
        """
        message = event.get("message", {})

        # ✅ Send the message directly (no extra wrapping)
        await self.send(text_data=json.dumps(message))
        print(f"📩 Sent to {getattr(self.scope['user'], 'username', 'unknown')}: {message}")
