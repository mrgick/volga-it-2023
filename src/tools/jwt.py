from datetime import datetime

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from ..config import settings
from ..database import redis_client
from .exceptions import JWTException


class TokenDataCreate(BaseModel):
    sub: str
    exp: datetime


class TokenData(BaseModel):
    sub: int
    exp: datetime


class TokenResponse(BaseModel):
    token: str


class JWTPayload:
    def __init__(self):
        pass

    async def __call__(
        self, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ):
        try:
            payload = TokenData(
                **jwt.decode(authorization.credentials, settings.secret_key)
            )
        except JWTError:
            raise JWTException()
        except jwt.ExpiredSignatureError:
            raise JWTException("expired_token")
        except ValidationError:
            raise JWTException()
        if await redis_client.get(f"{payload.sub}|{authorization.credentials}"):
            raise JWTException("blocked_token")
        return payload
