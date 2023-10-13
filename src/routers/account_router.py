from fastapi import Depends
from fastapi.routing import APIRouter
from passlib.context import CryptContext

from ..schemas.account import CreateAccount, InfoAccount
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
    return await service.info(token_data)


@router.post("/SignIn")
def sign_in(
    token_data: TokenData = Depends(JWTPayload("client")),
):
    """Получение нового jwt токена пользователя"""
    pass


@router.post("/SignUp", response_model=TokenResponse)
async def sign_up(account: CreateAccount, service: AccountService = Depends()):
    """Регистрация нового аккаунта"""
    return await service.sign_up(account)


@router.post("/SignOut")
def sign_out():
    """Выход из аккаунта"""


@router.post("/Update")
def update():
    """Обновление своего аккаунта"""
