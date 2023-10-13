from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from ..config import settings
from ..database import AsyncSession, get_async_session
from ..models.account import Account
from ..schemas.account import CreateAccount, InfoAccount
from ..tools.exceptions import AlreadyExists, DoesntExists
from ..tools.jwt import TokenData, TokenDataCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AccountService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def info(self, token_data: TokenData) -> Account:
        stmt = select(Account).where(Account.id == token_data.sub)
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise DoesntExists(f"Account with id={token_data.sub} doesn't exists")
        return account

    async def sign_in(self, data: CreateAccount):
        # TODO: перенести логику создания токена сюда.
        pass

    async def sign_up(self, data: CreateAccount) -> InfoAccount:
        stmt = select(Account).filter_by(username=data.username)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise AlreadyExists(f"Username='{data.username}' already registered.")
        account = Account(
            username=data.username,
            hashed_password=pwd_context.hash(data.password),
            isAdmin=False,
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        payload = TokenDataCreate(
            sub=str(account.id), role="client", exp=datetime.now() + timedelta(days=30)
        )
        token = jwt.encode(
            payload.model_dump(),
            settings.secret_key,
        )
        return {"token": token}
