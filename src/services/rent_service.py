import math
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import exists, func, select
from sqlalchemy.orm import selectinload

from ..models.account import Account
from ..models.rent import PriceType, Rent
from ..models.transport import Transport, TransportType
from ..schemas.response import Success
from ..tools.exceptions import BadRequest, NotFound
from ..tools.jwt import TokenData
from . import BaseSevice


class RentService(BaseSevice):
    async def get_transport_list(
        self, lat: Decimal, long: Decimal, radius: float, transportType: TransportType
    ) -> list[Transport]:
        # Haversine formula for distance calculation
        haversine_formula = func.pow(
            func.sin(func.radians(Transport.latitude - lat) / 2), 2
        ) + func.cos(func.radians(lat)) * func.cos(
            func.radians(Transport.latitude)
        ) * func.pow(
            func.sin(func.radians(Transport.longitude - long) / 2), 2
        )
        # Earth radius is 6371 km
        haversine_distance = 2 * 6371 * func.asin(func.sqrt(haversine_formula))

        stmt = select(Transport).filter(
            Transport.transportType == transportType,
            Transport.isDeleted == False,  # noqa
            haversine_distance <= radius,
        )

        result = await self.session.execute(stmt)
        transports = result.scalars().all()

        return transports

    async def get_rent(self, rent_id: int, token_data: TokenData) -> Rent:
        stmt = select(Rent).filter_by(id=rent_id).options(selectinload(Rent.transport))
        result = await self.session.execute(stmt)
        rent = result.scalar_one_or_none()
        if rent is None:
            raise NotFound(f"Rent with id={rent_id} not found")
        if rent.userId != token_data.sub and rent.transport.ownerId != token_data.sub:
            raise BadRequest("You are not the renter or the owner of the transport")
        return rent

    async def get_account_history(self, account_id: int) -> list[Rent]:
        return await self.session.scalars(select(Rent).filter_by(userId=account_id))

    async def get_transport_history(
        self, transport_id: int, token_data: TokenData
    ) -> list[Rent]:
        stmt = (
            select(Transport)
            .filter_by(id=transport_id, ownerId=token_data.sub)
            .options(selectinload(Transport.rents))
        )
        result = await self.session.execute(stmt)
        transport = result.scalar_one_or_none()
        if transport is None:
            raise NotFound(f"Transport with id={transport_id} not found")
        elif transport.ownerId != token_data.sub:
            raise BadRequest("Transport owner is not you.")
        return transport.rents

    async def start_rent(
        self, transport_id: int, rent_type: PriceType, token_data: TokenData
    ) -> Rent:
        stmt = select(Transport).filter_by(id=transport_id, isDeleted=False)
        result = await self.session.execute(stmt)
        transport = result.scalar_one_or_none()
        if transport is None:
            raise BadRequest("Transport not found")
        elif not transport.canBeRented:
            raise BadRequest("Transport is already rented")
        elif transport.ownerId == token_data.sub:
            raise BadRequest("Owner cannot rent his transport")

        if rent_type == "Days":
            priceOfUnit = transport.dayPrice
            minBalance = priceOfUnit * 2
        else:
            priceOfUnit = transport.minutePrice
            minBalance = priceOfUnit * 1440
        if priceOfUnit is None:
            raise BadRequest(f"Price of {rent_type} is null.")

        stmt = (
            exists(Account)
            .select()
            .filter(Account.id == token_data.sub, Account.balance >= minBalance)
        )
        result = await self.session.execute(stmt)
        if not result.scalar():
            raise BadRequest(f"Account balance is less than {minBalance}")

        rent = Rent(
            transportId=transport_id,
            userId=token_data.sub,
            priceOfUnit=priceOfUnit,
            priceType=rent_type,
        )
        transport.canBeRented = False
        self.session.add(rent)
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(rent)
        return rent

    async def rent_end(self, rent_id: int, lat: Decimal, long: Decimal) -> Success:
        # get rent
        stmt = (
            select(Rent)
            .filter_by(id=rent_id, timeEnd=None)
            .options(
                selectinload(Rent.user),
                selectinload(Rent.transport).selectinload(Transport.owner),
            )
        )
        result = await self.session.execute(stmt)
        rent = result.scalar_one_or_none()
        if rent is None:
            raise NotFound("Opened rent not found")

        # calculate finalPrice
        rent.timeEnd = datetime.now(timezone.utc)
        timedelta = rent.timeEnd - rent.timeStart
        if rent.priceType == "Days":
            timedelta = timedelta.days + 1
        else:
            timedelta = math.ceil(timedelta.total_seconds() / 60)
        rent.finalPrice = rent.priceOfUnit * timedelta

        # swap balance beetween user and owner
        user: Account = rent.user
        owner: Account = rent.transport.owner
        user.balance -= rent.finalPrice
        owner.balance += rent.finalPrice

        # set that transport can be rented
        transport: Transport = rent.transport
        transport.canBeRented = True

        self.session.add(rent)
        self.session.add(user)
        self.session.add(owner)
        self.session.add(transport)
        await self.session.commit()
        return Success()

    async def rent_end_user(
        self, rent_id: int, lat: Decimal, long: Decimal, token_data: TokenData
    ) -> Success:
        if not await self.session.scalar(
            exists(Rent)
            .select()
            .where(Rent.id == rent_id, Rent.userId == token_data.sub)
        ):
            raise BadRequest("You are not the renter")
        return await self.rent_end(rent_id, lat, long)
