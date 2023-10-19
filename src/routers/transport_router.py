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


@router.get("/{transport_id}", response_model=TransportInfo)
async def get_transport(transport_id: PositiveInt, service: Service):
    """Получение информации о транспорте по id"""
    return await service.get_transport(transport_id)


@router.post("", response_model=TransportInfo)
async def create_transport(
    create_data: TransportCreate, token_data: UserToken, service: Service
):
    """Добавление нового транспорта"""
    return await service.create_transport(token_data, create_data)


@router.put("/{transport_id}", response_model=TransportInfo)
async def update_transport(
    transport_id: PositiveInt,
    update_data: TransportUpdate,
    token_data: UserToken,
    service: Service,
):
    """Изменение транспорта оп id"""
    return await service.update_transport(transport_id, token_data, update_data)


@router.delete("/{transport_id}", response_model=Success)
async def delete_transport(
    transport_id: PositiveInt, token_data: UserToken, service: Service
):
    """Удаление транспорта по id"""
    return await service.delete_transport(transport_id, token_data)
