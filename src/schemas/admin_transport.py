from pydantic import PositiveInt

from .transport import TransportCreate as _TransportCreate
from .transport import TransportInfo as _TransportInfo


class TransportInfo(_TransportInfo):
    pass


class TransportCreate(_TransportCreate):
    ownerId: PositiveInt


class TransportUpdate(TransportCreate):
    pass
