from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class OK(BaseModel, Generic[T]):
    ok: bool = True
    message: str = "ok"
    data: T


# {
#     id: 3,
#     name: '水溶解氧',
#     value: 5.5,
#     unit: 'mg/L',
#     type: 'oxygen',
#     status: 'online',
#     min: 0,
#     max: 10
#   },

class MonitorModel(BaseModel):
    id: int
    name: str
    value: float
    unit: str
    type: str
    status: str
    min: float
    max: float


# {
#   id: 1,
#   name: '进水电磁阀',
#   icon: 'valve-inlet.png',
#   status: 'online',
#   isOn: false
# },

class ControllerModel(BaseModel):
    id: int
    name: str
    icon: str
    status: str
    isOn: bool


class CommandModel(BaseModel):
    device: int
    command: str  # 1 or 0
