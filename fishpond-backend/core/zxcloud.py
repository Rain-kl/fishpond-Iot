# {"id":"780392644007","server":"api.zhiyun360.com","key":"dnsGB3p0dQAFBwN0RA1ABw0DDgw"}
# wss://api.zhiyun360.com:28090/

import json
from config import uid, key
import websockets
from loguru import logger


class WebSocketClient:
    def __init__(self):
        self.url = "wss://api.zhiyun360.com:28090/"
        self.websocket = None
        self.authorization = {
            "method": "authenticate",
            "uid": uid,
            "key": key
        }

    async def connect(self):
        self.websocket = await websockets.connect(self.url)
        await self.send_data(self.authorization)
        logger.success("Connected!")

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
            await self.websocket.send(
                json.dumps(data, ensure_ascii=False)
            )
            logger.success("Process -> engine")

    async def receive_message(self):
        """
        从核心接收消息
        :return:
        """
        if self.websocket:
            try:
                response = await self.websocket.recv()
                return response
            except websockets.exceptions.ConnectionClosedError as e:
                logger.critical(f"连接已断开: {str(e)}")
                # 不在这里自动重连，让调用者决定如何处理连接断开
                return None
        else:
            logger.error("WebSocket连接不存在")
            return None

    async def close(self):
        if self.websocket:
            try:
                await self.websocket.close()
                logger.success("Connection closed!")
            except Exception as e:
                logger.error(f"关闭连接时出错: {str(e)}")


def create_client() -> WebSocketClient:
    return WebSocketClient()
