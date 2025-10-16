from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
import jwt


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware to authenticate WebSocket connections using JWT tokens.
    Token should be passed as a query parameter: ?token=<JWT>
    """

    async def __call__(self, scope, receive, send):
        # Extract token from query string
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_list = query_params.get("token")

        if token_list:
            token = token_list[0]
            try:
                # Decode JWT token using DRF SimpleJWT
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await self.get_user(user_id)
                scope["user"] = user
                print(f"✅ JWTAuthMiddleware authenticated user: {getattr(user, 'username', 'Anonymous')}")
            except jwt.ExpiredSignatureError:
                print("❌ JWT expired")
                scope["user"] = AnonymousUser()
            except Exception as e:
                print(f"❌ JWT decode error: {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        # Call the inner application
        return await super().__call__(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_user(user_id):
        """
        Fetch user from database asynchronously.
        Importing the model inside the function avoids early app loading errors.
        """
        from accounts.models import CustomUser
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return AnonymousUser()
