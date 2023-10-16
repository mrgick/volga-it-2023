from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CreateAccount(BaseModel):
    username: str = Field(max_length=255)
    password: str = Field(max_length=255)


class LoginAccount(CreateAccount):
    pass


class UpdateAccount(CreateAccount):
    pass


class InfoAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(max_length=255)
    balance: Decimal = Field(max_digits=10, decimal_places=2)
