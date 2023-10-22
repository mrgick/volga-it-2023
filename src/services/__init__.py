from fastapi import Depends

from ..database import AsyncSession, get_async_session


class BaseSevice:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
