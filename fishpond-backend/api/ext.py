import asyncio
import random
import time
from typing import Any

from loguru import logger

import api.available_device as available_device
from core.parser import parse_zx_response
from core.zdb import zx_db
from core.zxcloud import WebSocketClient, create_client
from .model import CommandModel
from .model import MonitorModel, ControllerModel


class GlobalWSClient:
    def __init__(self):
        self.client = None

    def set_client(self, client: WebSocketClient):
        self.client = client

    def get_client(self):
        return self.client


global_ws_client = GlobalWSClient()


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
        status="online",
        isOn=False
    ) for controller in available_device.controllers]


def generate_command(command: CommandModel) -> dict[str, str | Any] | None:
    """
    生成控制命令
    {"method":"control","addr":"00:12:4B:00:1F:5F:84:8C","data":"{CD1=1}"}
    :param command:
    :return:
    """

    for controller in available_device.controllers:
        if controller['id'] == command.device:
            addr = controller['addr']
            cmd_value = "1" if command.command == "1" else "0"
            if cmd_value == "1":
                cmd_json = {
                    "method": "control",
                    "addr": addr,
                    "data": f"{{OD1={controller['position']},D1=?}}"
                }
            else:
                cmd_json = {
                    "method": "control",
                    "addr": addr,
                    "data": f"{{CD1={controller['position']},D1=?}}"
                }
            return cmd_json
    return None


async def websocket_background_task(ws_client: WebSocketClient):
    max_reconnect_interval = 60  # 最大重连间隔（秒）

    # 连接成功后重置重试计数和间隔
    retry_count = 0
    reconnect_interval = 5
    while True:
        try:
            # 接收消息
            response = await ws_client.receive_message()

            # 如果成功接收到消息，则处理它
            if response:
                result = parse_zx_response(response)
                if result:
                    logger.debug(f"成功处理消息: {response}")
                else:
                    logger.warning(f"消息处理返回空结果: {response}")

                # 成功处理消息后继续循环，不要重建连接
                continue

        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
            retry_count += 1

            # 安全地关闭连接
            if ws_client:
                try:
                    await ws_client.close()
                except Exception as close_error:
                    logger.error(f"关闭连接出错: {str(close_error)}")
                finally:
                    ws_client = None

            # 使用指数退避策略计算下次重连间隔
            reconnect_interval = min(reconnect_interval * 1.5, max_reconnect_interval)
            wait_time = reconnect_interval

            logger.info(f"将在 {wait_time} 秒后尝试重新连接 (重试 #{retry_count})")
            await asyncio.sleep(wait_time)


async def timed_control(device_id: int, duration: int):
    """
    定时控制设备函数，开启设备后等待指定时间再关闭
    :param device_id: 设备ID
    :param duration: 运行时长（秒）
    :return: 执行结果
    """
    try:
        # 创建WebSocket客户端并连接
        ws_client = create_client()
        await ws_client.connect()

        if not ws_client:
            return {"success": False, "message": "WebSocket 连接失败"}

        # 构建并发送开启命令
        open_command = CommandModel(device=device_id, command="1")
        open_cmd_json = generate_command(open_command)
        if not open_cmd_json:
            return {"success": False, "message": "无法找到指定设备"}

        await ws_client.send_data(open_cmd_json)
        logger.info(f"设备 {device_id} 已开启，将在 {duration} 秒后关闭")

        # 等待指定时间
        await asyncio.sleep(duration)

        # 构建并发送关闭命令
        close_command = CommandModel(device=device_id, command="0")
        close_cmd_json = generate_command(close_command)
        await ws_client.send_data(close_cmd_json)
        logger.info(f"设备 {device_id} 已自动关闭")

        return {"success": True, "message": "定时控制完成", "duration": duration}
    except Exception as e:
        logger.error(f"定时控制出错: {str(e)}")
        return {"success": False, "message": f"定时控制出错: {str(e)}"}
