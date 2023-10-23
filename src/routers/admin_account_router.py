from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..schemas.admin_account import Account, CreateAccount, UpdateAccount
from ..schemas.response import Success
from ..services.admin_account_service import AdminAccountService
from ..tools.jwt import JWTPayload

router = APIRouter(
    prefix="/Account",
    tags=["AdminAccountController"],
    dependencies=[Depends(JWTPayload(is_admin=True))],
)
Service = Annotated[AdminAccountService, Depends()]


@router.get("", response_model=list[Account])
async def get_list_accounts(start: PositiveInt, limit: PositiveInt, service: Service):
    """Получение списка всех неудаленных аккаунтов (start начинается с 0)"""
    return await service.get_list_accounts(start, limit)


@router.get("/{accountId}", response_model=Account)
async def get_account_detail(accountId: PositiveInt, service: Service):
    """Получение информации об аккаунте по id"""
    return await service.get_account(accountId)


@router.post("", response_model=Account)
async def create_account(account: CreateAccount, service: Service):
    """Создание администратором нового аккаунта"""
    return await service.create_account(account)


@router.put("/{accountId}", response_model=Account)
async def update_account(
    accountId: PositiveInt,
    account: UpdateAccount,
    service: Service,
):
    """
    Изменение администратором аккаунта по id
    (нельзя изменять username на уже существующий в системе)
    """
    return await service.update_account(accountId, account)


@router.delete("/{accountId}", response_model=Success)
async def delete_account(accountId: PositiveInt, service: Service):
    """
    Удаление аккаунта по id
    (Открытых аренд не должно быть;
    Впоследствии аккаунт и весь его транспорт становятся удалёнными)
    """
    return await service.delete_account(accountId)
