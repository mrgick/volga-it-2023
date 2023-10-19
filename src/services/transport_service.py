from fastapi import Depends
from sqlalchemy import select

from ..database import AsyncSession, get_async_session
from ..models.transport import Transport
from ..schemas.response import Success
from ..schemas.transport import TransportCreate, TransportUpdate
from ..tools.exceptions import BadRequest, NotFound
from ..tools.jwt import TokenData


class TransportService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_transport(self, transport_id) -> Transport:
        stmt = select(Transport).filter_by(id=transport_id)
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise NotFound(f"Transport with id={transport_id} not found")
        return account

    async def create_transport(
        self, token_data: TokenData, create_data: TransportCreate
    ) -> Transport:
        transport = Transport(ownerId=token_data.sub, **create_data.model_dump())
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def update_transport(
        self, transport_id: int, token_data: TokenData, update_data: TransportUpdate
    ) -> Transport:
        transport = await self.get_transport(transport_id)
        if transport.ownerId != token_data.sub:
            raise BadRequest("Transport owner is not you.")
        for field, value in update_data:
            setattr(transport, field, value)
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def delete_transport(
        self, transport_id: int, token_data: TokenData
    ) -> Success:
        transport = await self.get_transport(transport_id)
        if transport.ownerId != token_data.sub:
            raise BadRequest("Transport owner is not you.")
        elif transport.idDeleted:
            raise BadRequest("Transport is already deleted.")
        transport.isDeleted = True
        await self.session.commit()
        return Success()
