from datetime import datetime, timedelta
from django.conf import settings
import jwt
import uuid


class TokenService:
    @staticmethod
    def generate_token(user_id: uuid.UUID) -> str:
        expires_at = datetime.now() + timedelta(days=int(settings.DELTA_DAYS_FOR_TOKEN_TO_EXPIRE))
        token = jwt.encode({
            'id': user_id,
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
        return token

    @staticmethod
    def verify_token(token: str) -> bool:


        return False