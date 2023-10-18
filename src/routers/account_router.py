from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from ..schemas.account import CreateAccount, InfoAccount, LoginAccount, UpdateAccount
from ..schemas.response import Success
from ..services.account_service import AccountService
from ..tools.jwt import JWTPayload, TokenData, TokenResponse

router = APIRouter(prefix="/Account", tags=["AccountController"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get(
    "/Me",
    response_model=InfoAccount,
)
async def me(
    token_data: TokenData = Depends(JWTPayload()), service: AccountService = Depends()
):
    """Получение данных о текущем аккаунте"""
    return await service.info(token_data.sub)


@router.post("/SignIn", response_model=TokenResponse)
async def sign_in(account: LoginAccount, service: AccountService = Depends()):
    """Получение нового jwt токена пользователя"""
    return await service.sign_in(account)


@router.post("/SignUp", response_model=InfoAccount)
async def sign_up(account: CreateAccount, service: AccountService = Depends()):
    """Регистрация нового аккаунта"""
    return await service.sign_up(account)


@router.post("/SignOut", response_model=Success)
async def sign_out(
    token_data: TokenData = Depends(JWTPayload()),
    service: AccountService = Depends(),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """Выход из аккаунта"""
    return await service.sign_out(token_data, authorization.credentials)


@router.put("/Update", response_model=InfoAccount)
async def update(
    account: UpdateAccount,
    token_data: TokenData = Depends(JWTPayload()),
    service: AccountService = Depends(),
):
    """Обновление своего аккаунта"""
    return await service.update(account, token_data)
