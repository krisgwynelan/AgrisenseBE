# agrisense/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisense.settings")
django.setup()

# Import middleware and routing
from accounts.middleware import JWTAuthMiddleware
from agrisense.routing import websocket_urlpatterns  # <- import here

# Standard Django ASGI application for HTTP
django_asgi_app = get_asgi_application()

# Main ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
