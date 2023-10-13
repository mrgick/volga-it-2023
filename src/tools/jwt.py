from datetime import datetime
from typing import Literal

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from ..config import settings
from .exceptions import JWTException


class TokenDataCreate(BaseModel):
    sub: str
    role: Literal["client", "admin"] = "client"
    exp: datetime


class TokenData(BaseModel):
    sub: int
    role: Literal["client", "admin"]
    exp: datetime


class TokenResponse(BaseModel):
    token: str


ROLES = ["client", "admin"]
ROLES_TYPE = Literal["client", "admin"]


class JWTPayload:
    def __init__(self, role: ROLES_TYPE = "client"):
        if role not in ROLES:
            raise Exception("Указан неверный тип роли")
        self.role = role

    def __call__(
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
        if self.role == "admin" and payload.role != "admin":
            raise JWTException("invalid_role")
        return payload
