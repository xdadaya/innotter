from datetime import datetime

import jwt
from fastapi import HTTPException

from microservice.settings import settings


class TokenVerify:
    @staticmethod
    def token_verify(authorization: str) -> bool:
        token_header, token = authorization.split(" ")
        if token_header.lower() != settings.AUTHENTICATION_HEADER_PREFIX.lower():
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM)
        except Exception:
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')

        if payload["exp"] < int(datetime.now().timestamp()):
            raise HTTPException(status_code=403, detail='Token is expired')

        return payload["id"]
