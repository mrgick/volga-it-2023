from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from ..config import settings
from ..database import AsyncSession, get_async_session, redis_client
from ..models.account import Account
from ..schemas.account import CreateAccount, LoginAccount, UpdateAccount
from ..schemas.response import Success
from ..tools.exceptions import AlreadyExists, BadRequest, NotFound
from ..tools.jwt import TokenData, TokenDataCreate, TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AccountService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def info(self, account_id) -> Account:
        stmt = select(Account).where(
            Account.id == account_id, Account.is_deleted is False
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise NotFound(f"Account with id={account_id} not found")
        return account

    async def sign_in(self, data: LoginAccount) -> TokenResponse:
        stmt = select(Account).where(
            Account.username == data.username, Account.is_deleted is False
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None or not pwd_context.verify(
            data.password, account.hashed_password
        ):
            raise BadRequest("Incorrect login or password")

        payload = TokenDataCreate(
            sub=str(account.id), role="client", exp=datetime.now() + timedelta(days=30)
        )
        token = jwt.encode(
            payload.model_dump(),
            settings.secret_key,
        )
        return TokenResponse(token=token)

    async def sign_up(self, data: CreateAccount) -> Account:
        stmt = select(Account).where(
            Account.username == data.username, Account.is_deleted is False
        )
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise AlreadyExists(f"Username='{data.username}' already registered.")
        account = Account(
            username=data.username, hashed_password=pwd_context.hash(data.password)
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def sign_out(self, token_data: TokenData, credentials: str) -> Success:
        await redis_client.set(f"{token_data.sub}|{credentials}", "True")
        return Success()

    async def update(self, data: UpdateAccount, token_data: TokenData) -> Account:
        account = await self.info(token_data.sub)
        stmt = select(Account).where(
            Account.username == data.username, Account.is_deleted is False
        )
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise AlreadyExists(f"Username='{data.username}' already registered.")

        account.username = data.username
        account.hashed_password = pwd_context.hash(data.password)

        self.session.add(account)
        try:
            await self.session.commit()
        except Exception as e:
            raise BadRequest(str(e))
        await self.session.refresh(account)
        return account
