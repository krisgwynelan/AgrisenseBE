# agrisense/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json, random, asyncio

class SoilConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.user = user
        self.group_name = f"user_{user.id}_soil"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ Soil WebSocket connected for user {user.username}")

        asyncio.create_task(self.send_fake_soil_data())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"❌ Soil WebSocket disconnected for {self.user.username}")

    async def soil_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "soil_update",
            "data": event["data"]
        }))

    async def send_fake_soil_data(self):
        while True:
            await asyncio.sleep(5)
            data = {
                "temperature": round(random.uniform(25, 35), 1),
                "ph": round(random.uniform(5.5, 7.5), 1),
                "nitrogen": random.randint(10, 50),
                "phosphorus": random.randint(10, 50),
                "potassium": random.randint(10, 50),
            }
            await self.channel_layer.group_send(
                self.group_name, {"type": "soil_update", "data": data}
            )
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{user.id}_notifications"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ Notification WS connected for {user.username}")

    async def daily_summary(self, event):
        await self.send(text_data=json.dumps({
            "type": "daily_summary",
            "title": event["title"],
            "message": event["message"],
            "summary": event["summary"],
            "date": event["date"],
        }))
