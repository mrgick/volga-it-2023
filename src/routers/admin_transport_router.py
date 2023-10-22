from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..models.transport import TransportType
from ..schemas.admin_transport import TransportCreate, TransportInfo, TransportUpdate
from ..schemas.response import Success
from ..services.admin_transport_service import AdminTransportService
from ..tools.jwt import JWTPayload

router = APIRouter(
    prefix="/Transport",
    tags=["AdminTransportController"],
    dependencies=[Depends(JWTPayload(is_admin=True))],
)
Service = Annotated[AdminTransportService, Depends()]


@router.get("/", response_model=list[TransportInfo])
async def get_transport_list(
    start: PositiveInt,
    count: PositiveInt,
    transportType: TransportType,
    service: Service,
):
    """Получение списка всех неудаленных транспортных средств"""
    return await service.get_transport_list(start, count, transportType)


@router.get("/{transportId}", response_model=TransportInfo)
async def get_transport(transportId: PositiveInt, service: Service):
    """Получение информации о транспорте по id"""
    return await service.get_transport(transportId)


@router.post("", response_model=TransportInfo)
async def create_transport(create_data: TransportCreate, service: Service):
    """Добавление нового транспорта"""
    return await service.create_transport(create_data)


@router.put("/{transportId}", response_model=TransportInfo)
async def update_transport(
    transportId: PositiveInt,
    update_data: TransportUpdate,
    service: Service,
):
    """Изменение транспорта оп id"""
    return await service.update_transport(transportId, update_data)


@router.delete("/{transportId}", response_model=Success)
async def delete_transport(transportId: PositiveInt, service: Service):
    """Удаление транспорта по id"""
    return await service.delete_transport(transportId)
