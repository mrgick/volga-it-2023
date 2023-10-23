from fastapi import Depends
from sqlalchemy import exists, select

from ..database import AsyncSession, get_async_session
from ..models.account import Account
from ..schemas.response import Success
from ..tools.exceptions import BadRequest, NotFound
from ..tools.jwt import TokenData


class PaymentService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def hesoyam(self, account_id: int, token_data: TokenData) -> Success:
        if account_id != token_data.sub:
            stmt = exists(Account).select().filter_by(id=token_data.sub, isAdmin=True)
            result = await self.session.execute(stmt)
            if not result.scalar():
                raise BadRequest("Only admin can add balance to other users")
        stmt = select(Account).filter_by(id=account_id)
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account is None:
            raise NotFound(f"Account with id={account_id} not found")
        if account.balance + 250000 > 99999999:
            raise BadRequest("Maximum account can be 99999999.99")
        account.balance += 250000
        self.session.add(account)
        await self.session.commit()
        return Success()
