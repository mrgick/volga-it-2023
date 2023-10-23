from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..schemas.admin_rent import RentCreate, RentUpdate
from ..schemas.rent import RentEnd, RentInfo
from ..schemas.response import Success
from ..services.admin_rent_service import AdminRentService
from ..tools.jwt import JWTPayload

router = APIRouter(
    prefix="/Rent",
    tags=["AdminRentController"],
    dependencies=[Depends(JWTPayload(is_admin=True))],
)
Service = Annotated[AdminRentService, Depends()]


@router.get("/UserHistory/{userId}", response_model=list[RentInfo])
async def get_user_history(userId: PositiveInt, service: Service):
    """Получение истории аренд пользователя с id={userId}"""
    return await service.get_account_history(userId)


@router.get("/TransportHistory/{transportId}", response_model=list[RentInfo])
async def get_transport_history(transportId: PositiveInt, service: Service):
    """Получение истории аренд транспорта с id={transportId}"""
    return await service.get_transport_history(transportId)


@router.get("/{rentId}", response_model=RentInfo)
async def get_rent(rentId: PositiveInt, service: Service):
    """Получение информации по аренде по id"""
    return await service.get_rent(rentId)


@router.post("", response_model=RentInfo)
async def rent_create(create_data: RentCreate, service: Service):
    """
    Создание новой аренды
    (Пользователь и транспорт должны существовать;
    Пользователь не должен быть собственником транспорта;
    Если создается аренда не завершенной, то транспорт должен быть доступен для аренды)
    """
    return await service.create_rent(create_data)


@router.post("/End/{rentId}", response_model=Success)
async def rent_end(rentId: PositiveInt, end_data: RentEnd, service: Service):
    """
    Завершение аренды транспорта по id аренды
    (По аналогии, как метод у пользователя)
    """
    return await service.rent_end(rentId, end_data.lat, end_data.long)


@router.put("/{rentId}", response_model=RentInfo)
async def rent_update(rentId: PositiveInt, update_data: RentUpdate, service: Service):
    """
    Изменение записи об аренде по id
    (Изменяется только запись аренды в базе данных,
    все остальные действия на усмотрения администратора)
    """
    return await service.update_rent(rentId, update_data)


@router.delete("/{rentId}", response_model=Success)
async def rent_delete(rentId: PositiveInt, service: Service):
    """
    Удаление информации об аренде по id
    (Полностью удаляется из системы)
    """
    return await service.delete_rent(rentId)
