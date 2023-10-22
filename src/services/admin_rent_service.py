from sqlalchemy import delete, exists, select

from ..models.account import Account
from ..models.rent import Rent
from ..models.transport import Transport
from ..schemas.admin_rent import RentCreate, RentUpdate
from ..schemas.response import Success
from ..tools.exceptions import BadRequest, NotFound
from .rent_service import RentService


class AdminRentService(RentService):
    async def get_rent(self, rent_id: int) -> Rent:
        rent = await self.session.scalar(select(Rent).filter_by(id=rent_id))
        if rent is None:
            raise NotFound("Rent with not found")
        return rent

    async def get_transport_history(self, transport_id: int) -> list[Rent]:
        return await self.session.scalars(
            select(Rent).filter_by(transportId=transport_id)
        )

    async def create_rent(self, create_data: RentCreate) -> Rent:
        if not await self.session.scalar(
            exists(Account).select().filter_by(id=create_data.userId)
        ):
            raise NotFound("User not found")
        transport = await self.session.scalar(
            select(Transport).filter_by(id=create_data.transportId)
        )
        if not transport:
            raise NotFound("Transport not found")
        elif create_data.timeEnd is not None and transport.canBeRented is False:
            raise BadRequest("Transport is already rented")
        elif transport.ownerId == create_data.userId:
            raise BadRequest("Owner cannot rent his transport")
        rent = Rent(**create_data.model_dump())
        transport.canBeRented = False
        self.session.add(transport)
        self.session.add(rent)
        await self.session.commit()
        await self.session.refresh(rent)
        return rent

    async def delete_rent(self, rent_id: int) -> Success:
        if not await self.session.scalar(exists(Rent).select().filter_by(id=rent_id)):
            raise NotFound("Rent with not found")
        stmt = delete(Rent).filter_by(id=rent_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return Success()

    async def update_rent(self, rent_id: int, update_data: RentUpdate) -> Rent:
        if not await self.session.scalar(
            exists(Account).select().filter_by(id=update_data.userId)
        ):
            raise NotFound("User not found")
        transport = await self.session.scalar(
            select(Transport).filter_by(id=update_data.transportId)
        )
        if not transport:
            raise NotFound("Transport not found")
        elif transport.ownerId == update_data.userId:
            raise BadRequest("Owner cannot rent his transport")

        rent = await self.get_rent(rent_id)
        for field, value in update_data:
            setattr(rent, field, value)
        self.session.add(rent)
        await self.session.commit()
        await self.session.refresh(rent)
        return rent
