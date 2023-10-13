from decimal import Decimal

from sqlalchemy import DECIMAL, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    isAdmin: Mapped[bool] = mapped_column(Boolean())
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0.00)
