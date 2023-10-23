from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints


class CreateAccount(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
    password: str = Field(max_length=255)


class LoginAccount(CreateAccount):
    pass


class UpdateAccount(CreateAccount):
    pass


class InfoAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
    username: str = Field(max_length=255)
    balance: Decimal = Field(max_digits=10, decimal_places=2)
