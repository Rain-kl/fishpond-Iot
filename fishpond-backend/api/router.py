# api/endpoints.py

import requests
from fastapi import APIRouter, Request, HTTPException

from config import uid
from core.zxcloud import create_client
from . import available_device
from .ext import (
    random_controller_data,
    get_monitor_data,
    generate_command,
    timed_control,
)
from .model import OK, CommandModel, TimedCMDModel

router = APIRouter()


@router.get("/status/monitor")
def get_monitor(request: Request):
    try:
        return OK(data=get_monitor_data())
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.get("/status/controller")
def get_controller(request: Request):
    try:
        return OK(data=random_controller_data())
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


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
    try:
        for controller in available_device.monitors:
            if controller["id"] == device:
                addr = controller["addr"]
                position = controller["position"]
                url = f"http://api.zhiyun360.com:8080/v2/feeds/{uid}/datastreams/{addr}_{position}?duration={duration}"
                try:
                    rsp = requests.get(url, timeout=5)  # 添加超时设置
                    rsp.raise_for_status()  # 检查HTTP响应状态
                    return rsp.json()
                except requests.exceptions.ConnectionError:
                    raise HTTPException(status_code=503, detail="无法连接到智云平台服务器，请检查网络连接")
                except requests.exceptions.Timeout:
                    raise HTTPException(status_code=504, detail="连接智云平台服务器超时，请稍后再试")
                except requests.exceptions.HTTPError as http_err:
                    raise HTTPException(status_code=502, detail=f"智云平台服务器返回错误: {http_err}")
                except ValueError:  # JSON解析错误
                    raise HTTPException(status_code=500, detail="解析智云平台响应数据失败")
        raise HTTPException(status_code=404, detail=f"未找到ID为{device}的设备")
    except HTTPException:
        raise  # 重新抛出HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史数据时出错: {str(e)}")