from decimal import Decimal
from typing import Literal, get_args

from sqlalchemy import DECIMAL, Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

TransportType = Literal["Car", "Bike", "Scooter"]


class Transport(Base):
    __tablename__ = "transport"

    id: Mapped[int] = mapped_column(primary_key=True)
    ownerId: Mapped[int] = mapped_column(ForeignKey("account.id"))
    canBeRented: Mapped[bool] = mapped_column(Boolean(), default=True)
    transportType: Mapped[str] = mapped_column(
        Enum(
            *get_args(TransportType),
            create_constraint=True,
            validate_strings=True,
            name="transportTypeEnum"
        )
    )
    model: Mapped[str] = mapped_column(String(255))
    color: Mapped[str] = mapped_column(String(255))
    identifier: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    latitude: Mapped[Decimal] = mapped_column(DECIMAL(8, 6))
    longitude: Mapped[Decimal] = mapped_column(DECIMAL(9, 6))
    minutePrice: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    dayPrice: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean(), default=False)

    owner = relationship("Account", back_populates="transports", lazy=True)
    rents = relationship("Rent", back_populates="transport", lazy=True)
