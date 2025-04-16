# api/endpoints.py
import json

from fastapi import APIRouter, Request
from config import uid
from core.zxcloud import create_client
import requests
from . import available_device
from .ext import random_controller_data, get_monitor_data, generate_command, global_ws_client
from .model import OK, CommandModel

router = APIRouter()


@router.get('/status/monitor')
def get_monitor(request: Request):
    return OK(data=get_monitor_data())


@router.get("/status/controller")
def get_controller(request: Request):
    return OK(
        data=random_controller_data()
    )


# {"method":"control","addr":"00:12:4B:00:1F:5F:84:8C","data":"{OD=1,D1=?}"}
@router.post("/controller/command")
async def controller_command(request: Request, command: CommandModel):
    try:
        ws_client = create_client()
        await ws_client.connect()
        if ws_client:
            cmd_json = generate_command(command)
            await ws_client.send_data(cmd_json)
            return OK(message="命令已发送", data={"success": True})
        else:
            return OK(message="WebSocket 未连接", data={"success": False})
    except Exception as e:
        return OK(message=f"发送命令时出错: {str(e)}", data={"success": False})


@router.get("/history")
async def get_history(request: Request, device: int, duration):
    for controller in available_device.monitors:
        if controller['id'] == device:
            addr = controller['addr']
            position = controller['position']
            url = f"http://api.zhiyun360.com:8080/v2/feeds/{uid}/datastreams/{addr}_{position}?duration={duration}"
            rsp = requests.get(url)
            return rsp.json()
    pass
