from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import exceptions
import jwt
import uuid


class TokenService:
    @staticmethod
    def generate_token(user_id: uuid.UUID) -> str:
        expires_at = datetime.now() + timedelta(days=int(settings.DELTA_DAYS_FOR_TOKEN_TO_EXPIRE))
        token = jwt.encode({
            'id': str(user_id),
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
        return token

    @staticmethod
    def verify_token(auth_header: list[bytes]) -> str:
        auth_header_prefix = settings.AUTHENTICATION_HEADER_PREFIX.lower()
        if not auth_header:
            return None
        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        print(type(auth_header[0]))
        print(type(auth_header[1]))
        prefix = auth_header[0].decode('utf-8')
        if prefix.lower() != auth_header_prefix:
            return None

        token = auth_header[1].decode('utf-8')
        return token
