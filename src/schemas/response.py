from pydantic import BaseModel


class Success(BaseModel):
    status: str = "ok"
