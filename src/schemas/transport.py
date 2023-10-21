from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from ..models.transport import TransportType


class TransportUpdate(BaseModel):
    model_config: ConfigDict(str_strip_whitespace=True)
    canBeRented: bool = True
    model: str = Field(max_length=255)
    color: str = Field(max_length=255)
    identifier: str = Field(max_length=255)
    description: str | None = None
    latitude: Decimal = Field(ge=-90, le=90, max_digits=8, decimal_places=6)
    longitude: Decimal = Field(ge=-180, le=180, max_digits=9, decimal_places=6)
    minutePrice: Annotated[
        Decimal, Field(ge=0.01, max_digits=10, decimal_places=2)
    ] | None = None
    dayPrice: Annotated[
        Decimal, Field(ge=0.01, max_digits=10, decimal_places=2)
    ] | None = None

    @model_validator(mode="after")
    def validate_minute_or_day_price_not_none(self) -> "TransportUpdate":
        if self.minutePrice is None and self.dayPrice is None:
            raise ValueError("At least one of minutePrice or dayPrice must be provided")
        return self


class TransportCreate(TransportUpdate):
    transportType: TransportType


class TransportInfo(TransportCreate):
    id: PositiveInt
    ownerId: PositiveInt
    isDeleted: bool
