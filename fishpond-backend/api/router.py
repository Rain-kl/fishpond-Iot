# api/endpoints.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from .ext import random_controller_data, get_monitor_data, ws_client, generate_command
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
        if ws_client and ws_client.websocket:
            await ws_client.send_data(generate_command(command))
            return OK(message="命令已发送", data={"success": True})
        else:
            return OK(message="WebSocket 未连接", data={"success": False})
    except Exception as e:
        return OK(message=f"发送命令时出错: {str(e)}", data={"success": False})
