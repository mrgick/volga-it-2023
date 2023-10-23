from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..schemas.account import CreateAccount, InfoAccount, LoginAccount, UpdateAccount
from ..schemas.response import Success
from ..services.account_service import AccountService
from ..tools.dependencies import UserToken
from ..tools.jwt import TokenResponse

router = APIRouter(prefix="/Account", tags=["AccountController"])
Service = Annotated[AccountService, Depends()]


@router.get(
    "/Me",
    response_model=InfoAccount,
)
async def me(token_data: UserToken, service: Service):
    """Получение данных о текущем аккаунте"""
    return await service.info(token_data.sub)


@router.post("/SignIn", response_model=TokenResponse)
async def sign_in(account: LoginAccount, service: Service):
    """
    Получение нового jwt токена пользователя
    (Пользователь должен быть неудален)
    """
    return await service.sign_in(account)


@router.post("/SignUp", response_model=InfoAccount)
async def sign_up(account: CreateAccount, service: Service):
    """Регистрация нового аккаунта"""
    return await service.sign_up(account)


@router.post("/SignOut", response_model=Success)
async def sign_out(
    token_data: UserToken,
    service: Service,
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """
    Выход из аккаунта
    (Блокировка токена)
    """
    return await service.sign_out(token_data, authorization.credentials)


@router.put("/Update", response_model=InfoAccount)
async def update(
    account: UpdateAccount,
    token_data: UserToken,
    service: Service,
):
    """
    Обновление своего аккаунта
    (нельзя использовать уже используемые в системе username)
    """
    return await service.update(account, token_data)
