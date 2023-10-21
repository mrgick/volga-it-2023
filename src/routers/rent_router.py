from decimal import Decimal
from typing import Annotated

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from pydantic import PositiveFloat, PositiveInt

from ..models.transport import TransportType
from ..schemas.rent import RentEnd, RentInfo, RentStart
from ..schemas.response import Success
from ..schemas.transport import TransportInfo
from ..services.rent_service import RentService
from ..tools.dependencies import UserToken

router = APIRouter(prefix="/Rent", tags=["RentController"])
Service = Annotated[RentService, Depends()]


@router.get("/Transport", response_model=list[TransportInfo])
async def get_transport_list(
    type: TransportType,
    service: Service,
    radius: PositiveFloat = Query(description="Радиус в километрах"),
    lat: Decimal = Query(ge=-90, le=90, max_digits=8, decimal_places=6),
    long: Decimal = Query(ge=-180, le=180, max_digits=9, decimal_places=6),
):
    """Получение транспорта доступного для аренды по параметрам"""
    return await service.get_transport_list(lat, long, radius, type)


@router.get("/MyHistory", response_model=list[RentInfo])
async def get_account_history(service: Service, token_data: UserToken):
    """Получение информации об аренде по id"""
    return await service.get_account_history(token_data)


@router.get("/TransportHistory/{transportId}", response_model=list[RentInfo])
async def get_transport_history(
    transportId: PositiveInt, service: Service, token_data: UserToken
):
    """Получение истории аренд транспорта"""
    return await service.get_transport_history(transportId, token_data)


@router.post("/New/{transportId}", response_model=RentInfo)
async def start_rent(
    transportId: PositiveInt,
    rent_start: RentStart,
    service: Service,
    token_data: UserToken,
):
    """Аренда транспорта в личное пользование"""
    return await service.start_rent(transportId, rent_start.rentType, token_data)


@router.post("/End/{rentId}", response_model=Success)
async def end_rent(
    rentId: PositiveInt, rent_end: RentEnd, service: Service, token_data: UserToken
):
    """Завершение аренды транспорта по id аренды"""
    return await service.rent_end(rentId, rent_end.lat, rent_end.long, token_data)


@router.get("/{rentId}", response_model=RentInfo)
async def get_rent(rentId: PositiveInt, service: Service, token_data: UserToken):
    """Получение информации об аренде по id"""
    return await service.get_rent(rentId, token_data)
