from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(max_length=255)
    balance: Decimal = Field(max_digits=10, decimal_places=2)
    isAdmin: bool
    isDeleted: bool
    id: PositiveInt


class CreateAccount(BaseModel):
    username: str = Field(max_length=255)
    password: str = Field(max_length=255)
    balance: Decimal = Field(max_digits=10, decimal_places=2)
    isAdmin: bool = False


class UpdateAccount(CreateAccount):
    pass
