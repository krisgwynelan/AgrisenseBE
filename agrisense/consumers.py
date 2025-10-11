import json
from channels.generic.websocket import AsyncWebsocketConsumer


# 🔔 Notification Consumer
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connected to notifications websocket"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "title": event.get("title", "Notification"),
            "message": event.get("message", "")
        }))


# 🌱 Soil Consumer
class SoilConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("soil_data", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connected to soil_data websocket"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("soil_data", self.channel_name)

    # ✅ Supports both 'soil_update' and 'send_sensor_data' types
    async def soil_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "soil_update",
            "data": event.get("data", {})
        }))

    async def send_sensor_data(self, event):
        await self.send(text_data=json.dumps({
            "type": "soil_update",
            "data": event.get("data", {})
        }))
