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
            raise exceptions.AuthenticationFailed('Authentication error. Unable to decode token')

        if payload["exp"] < int(datetime.now().timestamp()):
            raise exceptions.AuthenticationFailed('Token is expired')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('There is no user with that token.')

        if user.is_blocked:
            raise exceptions.AuthenticationFailed('This user is blocked.')

        return user, token
