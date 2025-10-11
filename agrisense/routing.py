from django.urls import re_path
from agrisense.consumers import SoilConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/soil/$', SoilConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
