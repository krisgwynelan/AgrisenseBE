# accounts/middleware.py
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from channels.db import database_sync_to_async

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Default user
        scope["user"] = AnonymousUser()

        # Parse token from query string
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token_list = params.get("token")

        if token_list:
            token = token_list[0]
            print("🔑 WS Token received:", token[:20], "...")  # debug first 20 chars
            try:
                # Decode JWT
                access_token = AccessToken(str(token))
                user_id = access_token.get("user_id") or access_token.get("id")
                print("🔑 Extracted user_id:", user_id)

                if not user_id:
                    print("❌ No user_id in token")
                else:
                    user = await self.get_user(user_id)
                    if user and user.is_active:
                        scope["user"] = user
                        print(f"✅ WS Authenticated as {user.username}")
                    else:
                        print("⚠️ Invalid or inactive user")
            except TokenError as e:
                print(f"❌ Invalid JWT: {e}")
        else:
            print("⚠️ No token provided")

        # Call the next middleware / consumer
        return await super().__call__(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
