import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User
from django.http import HttpRequest


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = settings.AUTHENTICATION_HEADER_PREFIX

    def authenticate(self, request: HttpRequest) -> (User, str):
        auth_header = authentication.get_authorization_header(request).split()
        print(auth_header)
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        print(prefix)
        token = auth_header[1].decode('utf-8')
        print(token)

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request: HttpRequest, token: str) -> (User, str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM)
        except Exception:
            msg = 'Authentication error. Unable to decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'There is no user with that token.'
            raise exceptions.AuthenticationFailed(msg)
        return user, token
