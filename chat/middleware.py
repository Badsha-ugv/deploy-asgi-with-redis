from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user_from_token(token):
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        return user
    except (InvalidToken, TokenError):
        return AnonymousUser()

class JWTMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = None
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf-8')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)