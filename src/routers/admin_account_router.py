from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt

from ..schemas.admin_account import Account, CreateAccount, UpdateAccount
from ..schemas.response import Success
from ..services.admin_account_service import AdminAccountService
from ..tools.dependencies import AdminToken

router = APIRouter(prefix="/Admin/Account", tags=["AdminAccountController"])
Service = Annotated[AdminAccountService, Depends()]


@router.get("", response_model=list[Account])
async def get_list_accounts(
    start: PositiveInt, limit: PositiveInt, token_data: AdminToken, service: Service
):
    """Получение списка всех неудаленных аккаунтов"""
    return await service.get_list_accounts(start, limit)


@router.get("/{account_id}", response_model=Account)
async def get_account_detail(
    account_id: PositiveInt, token_data: AdminToken, service: Service
):
    """Получение информации об аккаунте по id"""
    return await service.get_account(account_id)


@router.post("", response_model=Account)
async def create_account(
    account: CreateAccount, token_data: AdminToken, service: Service
):
    """Создание администратором нового аккаунта"""
    return await service.create_account(account)


@router.put("/{account_id}", response_model=Account)
async def update_account(
    account_id: PositiveInt,
    account: UpdateAccount,
    token_data: AdminToken,
    service: Service,
):
    """Изменение администратором аккаунта по id"""
    return await service.update_account(account_id, account)


@router.delete("/{account_id}", response_model=Success)
async def delete_account(
    account_id: PositiveInt, token_data: AdminToken, service: Service
):
    """Удаление аккаунта по id"""
    return await service.delete_account(account_id)