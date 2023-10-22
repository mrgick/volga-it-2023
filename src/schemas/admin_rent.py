from typing import ClassVar

from pydantic import model_validator

from .rent import RentInfo


class RentCreate(RentInfo):
    id: ClassVar[None] = None

    @model_validator(mode="after")
    def validate_model(self) -> "RentCreate":
        if self.timeEnd is not None and self.timeEnd <= self.timeStart:
            raise ValueError("timeEnd must be bigger that timeStart")
        if (
            self.timeEnd is not None
            and self.finalPrice is None
            or self.timeEnd is None
            and self.finalPrice is not None
        ):
            raise ValueError(
                "If one of timeEnd or finalPrice is given, the other must be given as well"
            )
        return self


class RentUpdate(RentCreate):
    pass
