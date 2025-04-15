import json
import random
import time
import asyncio
from core.zxcloud import create_client, WebSocketClient
from core.parser import parse_zx_response
from .model import MonitorModel, ControllerModel
import api.available_device as available_device
from .model import CommandModel
from core.zdb import zx_db
from loguru import logger

ws_client: WebSocketClient = None


def get_monitor_data():
    monitor_list = []
    for monitor in available_device.monitors:
        monitor_data = zx_db.search(addr=monitor["addr"])
        value = monitor_data.model_dump()[monitor["position"]]
        status = "offline"
        if int(time.time()) - int(monitor_data.updated) < 20:
            status = "online"

        model = MonitorModel(
            id=monitor['id'],
            name=monitor['name'],
            value=value,
            unit=monitor['unit'],
            type=monitor['type'],
            status=status,
            min=monitor['min'],
            max=monitor['max']
        )
        monitor_list.append(model)
    return monitor_list


def random_monitor_data():
    return [MonitorModel(
        id=monitor['id'],
        name=monitor['name'],
        value=random.uniform(monitor['min'], monitor['max']),
        unit=monitor['unit'],
        type=monitor['type'],
        status=random.choice(['online', 'offline']),
        min=monitor['min'],
        max=monitor['max']
    ) for monitor in available_device.monitors]


def random_controller_data():
    return [ControllerModel(
        id=controller['id'],
        name=controller['name'],
        icon=controller['icon'],
        status=random.choice(['online', 'offline']),
        isOn=random.choice([True, False])
    ) for controller in available_device.controllers]


def generate_command(command: CommandModel):
    """
    {"method":"control","addr":"00:12:4B:00:1F:5F:84:8C","data":"{OD=1,D1=?}"}
    :param command:
    :return:
    """
    for controller in available_device.controllers:
        if controller['name'] == command.device:
            addr = controller['addr']
            return json.dumps({
                "method": "control",
                "addr": addr,
                "data": f"{{OD={controller['position']},D1=?}}"
            })


async def websocket_background_task():
    global ws_client
    ws_client = create_client()
    await ws_client.connect("wss://api.zhiyun360.com:28090/")

    while True:
        try:
            response = await ws_client.receive_message()
            parse_zx_response(response)
            logger.debug(f"Received message: {response}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # 等待5秒后重连
            await ws_client.connect("wss://api.zhiyun360.com:28090/")
