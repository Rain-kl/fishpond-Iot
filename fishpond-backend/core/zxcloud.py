# {"id":"780392644007","server":"api.zhiyun360.com","key":"dnsGB3p0dQAFBwN0RA1ABw0DDgw"}
# wss://api.zhiyun360.com:28090/

import json
import time
from datetime import datetime

import websockets
from loguru import logger

from config import uid, key


class WebSocketClient:
    def __init__(self):
        self.url = "wss://api.zhiyun360.com:28090/"
        self.websocket = None
        self.authorization = {"method": "authenticate", "uid": uid, "key": key}
        self.last_log_time = 0  # 添加时间跟踪变量，用于限制日志记录频率

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            await self.send_data(self.authorization)
            logger.success("Connected!")
        except Exception as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def is_connected(self):
        """
        检查WebSocket连接是否正常
        """
        if self.websocket is None:
            return False
        try:
            # 通过检查连接状态而不是直接访问closed属性
            return self.websocket.open
        except AttributeError:
            # 如果open属性不可用，尝试其他方法判断连接状态
            try:
                return not self.websocket.closed
            except AttributeError:
                # 如果都不可用，假设连接已关闭
                return False

    async def send_data(self, data: dict | list):
        """
        发送原始消息到智云
        :param data:
        :return:
        """
        if self.websocket:
            await self.websocket.send(json.dumps(data, ensure_ascii=False))
            logger.success("Process -> engine")

    async def receive_message(self):
        """
        从核心接收消息
        :return:
        """
        if self.websocket:
            try:
                response = await self.websocket.recv()

                # 限制日志记录频率，每60秒只记录一次
                current_time = time.time()
                if current_time - self.last_log_time >= 60:
                    logger.info(
                        f"接收到服务器消息 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    self.last_log_time = current_time

                return response
            except websockets.exceptions.ConnectionClosedError as e:
                logger.critical(f"连接已断开: {str(e)}")
                raise ConnectionError("WebSocket连接已断开")
        else:
            logger.error("WebSocket连接不存在")
            raise ConnectionError("WebSocket<UNK>")

    async def close(self):
        if self.websocket:
            try:
                await self.websocket.close()
                logger.success("Connection closed!")
            except Exception as e:
                logger.error(f"关闭连接时出错: {str(e)}")


def create_client() -> WebSocketClient:
    return WebSocketClient()
