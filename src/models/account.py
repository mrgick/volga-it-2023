from decimal import Decimal

from sqlalchemy import DECIMAL, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    isAdmin: Mapped[bool] = mapped_column(Boolean(), default=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0.00)
    isDeleted: Mapped[bool] = mapped_column(Boolean(), default=False)

    transports = relationship("Transport", back_populates="owner", lazy=True)
    rents = relationship("Rent", back_populates="user", lazy=True)
