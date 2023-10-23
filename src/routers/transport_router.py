from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..schemas.response import Success
from ..schemas.transport import TransportCreate, TransportInfo, TransportUpdate
from ..services.transport_service import TransportService
from ..tools.dependencies import UserToken

router = APIRouter(prefix="/Transport", tags=["TransportController"])
Service = Annotated[TransportService, Depends()]


@router.get("/{transportId}", response_model=TransportInfo)
async def get_transport(transportId: PositiveInt, service: Service):
    """Получение информации о транспорте по id"""
    return await service.get_transport(transportId)


@router.post("", response_model=TransportInfo)
async def create_transport(
    create_data: TransportCreate, token_data: UserToken, service: Service
):
    """Добавление нового транспорта"""
    return await service.create_transport(token_data, create_data)


@router.put("/{transportId}", response_model=TransportInfo)
async def update_transport(
    transportId: PositiveInt,
    update_data: TransportUpdate,
    token_data: UserToken,
    service: Service,
):
    """Изменение собственного неудаленного транспорта оп id"""
    return await service.update_transport(transportId, token_data, update_data)


@router.delete("/{transportId}", response_model=Success)
async def delete_transport(
    transportId: PositiveInt, token_data: UserToken, service: Service
):
    """Удаление транспорта по id"""
    return await service.delete_transport(transportId, token_data)
