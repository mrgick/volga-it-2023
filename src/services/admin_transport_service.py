from fastapi import Depends
from sqlalchemy import exists, select

from ..database import AsyncSession, get_async_session
from ..models.account import Account
from ..models.transport import Transport
from ..schemas.admin_transport import TransportCreate, TransportUpdate
from ..schemas.response import Success
from ..tools.exceptions import BadRequest, NotFound


class AdminTransportService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_transport_list(
        self, start: int, count: int, transportType: str
    ) -> list[Transport]:
        stmt = (
            select(Transport)
            .filter_by(isDeleted=False, transportType=transportType)
            .offset(offset=start)
            .limit(limit=count)
        )
        result = await self.session.execute(stmt)
        return result.scalars()

    async def get_transport(self, transport_id) -> Transport:
        stmt = select(Transport).filter_by(id=transport_id)
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise NotFound(f"Transport with id={transport_id} not found")
        return account

    async def account_exists(self, ownerId: str):
        stmt = exists(Account).select().filter_by(id=ownerId, isDeleted=False)
        result = await self.session.execute(stmt)
        if not result.scalar():
            raise NotFound(f"Account with id={ownerId} not found")

    async def create_transport(self, create_data: TransportCreate) -> Transport:
        await self.account_exists(create_data.ownerId)
        transport = Transport(**create_data.model_dump())
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def update_transport(
        self, transport_id: int, update_data: TransportUpdate
    ) -> Transport:
        await self.account_exists(update_data.ownerId)
        transport = await self.get_transport(transport_id)
        for field, value in update_data:
            setattr(transport, field, value)
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def delete_transport(self, transport_id: int) -> Success:
        transport = await self.get_transport(transport_id)
        if transport.isDeleted:
            raise BadRequest("Transport is already deleted.")
        transport.isDeleted = True
        transport.canBeRented = False
        await self.session.commit()
        return Success()
