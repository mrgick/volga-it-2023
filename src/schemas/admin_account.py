from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints


class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(max_length=255)
    balance: Decimal = Field(ge=0.01, max_digits=10, decimal_places=2)
    isAdmin: bool
    isDeleted: bool
    id: PositiveInt


class CreateAccount(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
    password: str = Field(max_length=255)
    balance: Decimal = Field(ge=0.01, max_digits=10, decimal_places=2)
    isAdmin: bool = False


class UpdateAccount(CreateAccount):
    pass
