from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..schemas.response import Success
from ..services.payment_service import PaymentService
from ..tools.dependencies import UserToken

router = APIRouter(prefix="/Payment", tags=["PaymentController"])
Service = Annotated[PaymentService, Depends()]


@router.get("/Hesoyam/{accountId}", response_model=Success)
async def get_transport_list(
    accountId: PositiveInt, token_data: UserToken, service: Service
):
    """
    Добавляет на баланс аккаунта с id={accountId} 250 000 денежных единиц
    (Администратор может добавить баланс всем, обычный пользователь только себе)
    """
    return await service.hesoyam(accountId, token_data)
