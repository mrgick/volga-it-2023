from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt
from typing_extensions import Annotated

from ..models.rent import PriceType


class RentInfo(BaseModel):
    id: PositiveInt
    transportId: PositiveInt
    userId: PositiveInt
    timeEnd: datetime | None
    priceOfUnit: Decimal = Field(ge=0.01, max_digits=10, decimal_places=2)
    priceType: PriceType
    finalPrice: Annotated[
        Decimal, Field(ge=0.01, max_digits=10, decimal_places=2)
    ] | None


class RentStart(BaseModel):
    rentType: PriceType


class RentEnd(BaseModel):
    lat: Decimal = Field(ge=-90, le=90, max_digits=8, decimal_places=6)
    long: Decimal = Field(ge=-180, le=180, max_digits=9, decimal_places=6)
