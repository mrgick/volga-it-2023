from datetime import timedelta

from fastapi import Depends
from sqlalchemy import exists, select

from ..database import AsyncSession, get_async_session, redis_client
from ..models.account import Account
from ..models.rent import Rent  # noqa
from ..models.transport import Transport  # noqa
from ..schemas.admin_account import CreateAccount, UpdateAccount
from ..schemas.response import Success
from ..tools import pwd_context
from ..tools.exceptions import AlreadyExists, NotFound


class AdminAccountService:
    def __init__(
        self, session: AsyncSession = Depends(get_async_session)
    ) -> list[Account]:
        self.session = session

    async def get_list_accounts(self, start: int, count: int) -> list[Account]:
        stmt = (
            select(Account)
            .where(Account.isDeleted == False)  # noqa
            .offset(offset=start)
            .limit(limit=count)
        )  # noqa
        result = await self.session.execute(stmt)
        return result.scalars()

    async def get_account(self, account_id) -> Account:
        stmt = select(Account).where(Account.id == account_id)
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise NotFound(f"Account with id={account_id} not found")
        return account

    async def account_exists(self, username: str) -> bool:
        stmt = (
            exists(Account)
            .select()
            .where(Account.username == username, Account.isDeleted == False)  # noqa
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_account(self, data: CreateAccount) -> Account:
        if await self.account_exists(data.username):
            raise AlreadyExists(f"Username='{data.username}' already registered.")
        account = Account(
            username=data.username,
            hashed_password=pwd_context.hash(data.password),
            balance=data.balance,
            isAdmin=data.isAdmin,
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def update_account(self, account_id: int, data: UpdateAccount) -> Account:
        account = await self.get_account(account_id)
        if await self.account_exists(data.username):
            raise AlreadyExists(f"Username='{data.username}' already registered.")
        for field, value in data.model_dump(exclude=["password"]).items():
            setattr(account, field, value)
        account.hashed_password = pwd_context.hash(data.password)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def delete_account(self, account_id: int) -> Success:
        account = await self.get_account(account_id)
        account.isDeleted = True
        self.session.add(account)
        await self.session.commit()
        await redis_client.setex(f"{account_id}|isDeleted", timedelta(days=31), "True")
        return Success()