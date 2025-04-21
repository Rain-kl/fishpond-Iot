from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class OK(BaseModel, Generic[T]):
    ok: bool = True
    message: str = "ok"
    data: T
