# api/endpoints.py
from fastapi import APIRouter, Request

from .ext import random_controller_data, get_monitor_data
from .model import OK

router = APIRouter()


@router.get('/status/monitor')
def get_monitor(request: Request):
    return OK(data=get_monitor_data())


@router.get("/status/controller")
def get_controller(request: Request):
    return OK(
        data=random_controller_data()
    )


class CommandModel:
    device: str
    command: str


@router.post("/controller/command")
def controller_command(request: Request):
    pass
