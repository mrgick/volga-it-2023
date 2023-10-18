from typing import Annotated

from fastapi import Depends

from .jwt import JWTPayload, TokenData

UserToken = Annotated[TokenData, Depends(JWTPayload(is_admin=False))]
AdminToken = Annotated[TokenData, Depends(JWTPayload(is_admin=True))]
