from datetime import datetime
from decimal import Decimal
from typing import Literal, get_args

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

PriceType = Literal["Minutes", "Days"]


class Rent(Base):
    __tablename__ = "rent"

    id: Mapped[int] = mapped_column(primary_key=True)
    transportId: Mapped[int] = mapped_column(ForeignKey("transport.id"))
    userId: Mapped[int] = mapped_column(ForeignKey("account.id"))
    timeStart: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    timeEnd: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priceOfUnit: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    priceType: Mapped[PriceType] = mapped_column(
        Enum(
            *get_args(PriceType),
            name="priceTypeEnum",
            create_constraint=True,
            validate_strings=True
        )
    )
    finalPrice: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)

    transport = relationship("Transport", back_populates="rents")
    user = relationship("Account", back_populates="rents")
