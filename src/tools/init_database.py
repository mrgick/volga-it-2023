from sqlalchemy import select

from ..database import async_session, engine
from ..models import Base
from ..models.account import Account
from . import pwd_context


async def init_db(engine=engine):
    """Инициализация базы данных и создание аккаунта админа"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        account = await session.scalar(select(Account).filter_by(username="admin"))
        if account is None:
            account = Account(
                username="admin",
                hashed_password=pwd_context.hash("admin"),
                isAdmin=True,
            )
            session.add(account)
            await session.commit()
