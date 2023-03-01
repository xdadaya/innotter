from rest_framework import authentication, exceptions
from users.models import User
from django.http import HttpRequest
from users.token_service import TokenService
from innotter import settings
from datetime import datetime
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: HttpRequest) -> (User, str):
        auth_header = authentication.get_authorization_header(request).split()
        token = TokenService.verify_token(auth_header)
        if token is None:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request: HttpRequest, token: str) -> (User, str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM)
        except Exception:
            msg = 'Authentication error. Unable to decode token'
            raise exceptions.AuthenticationFailed(msg)

        if payload["exp"] < int(datetime.now().timestamp()):
            msg = "Token is expired"
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'There is no user with that token.'
            raise exceptions.AuthenticationFailed(msg)

        if user.is_blocked:
            msg = 'This user is blocked.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
