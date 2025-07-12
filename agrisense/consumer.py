# agrisense/consumer.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SoilDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("soil_data", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("soil_data", self.channel_name)

    async def send_sensor_data(self, event):
        await self.send(text_data=json.dumps({
            "type": "send_sensor_data",
            "data": event["data"]
        }))
