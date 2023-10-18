from datetime import datetime

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_async_session, redis_client
from ..models.account import Account
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
    def __init__(self, is_admin=False):
        self.is_admin = is_admin

    async def __call__(
        self,
        authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        session: AsyncSession = Depends(get_async_session),
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
        bad_token = await redis_client.get(f"{payload.sub}|{authorization.credentials}")
        deleted_user = await redis_client.get(f"{payload.sub}|isDeleted")
        if bad_token or deleted_user:
            raise JWTException("blocked_token")
        if self.is_admin:
            stmt = select(Account).where(
                Account.id == payload.sub, Account.isAdmin == True  # noqa
            )  # noqa
            result = await session.execute(stmt)
            if result.scalar_one_or_none() is None:
                raise JWTException("not_admin")
        return payload
