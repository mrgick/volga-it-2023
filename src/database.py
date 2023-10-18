from typing import AsyncGenerator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings
from .models import Base

engine = create_async_engine(str(settings.database_url))

async_session = async_sessionmaker(engine, expire_on_commit=False)
redis_client = redis.from_url(str(settings.redis_url))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def init_db(engine=engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
