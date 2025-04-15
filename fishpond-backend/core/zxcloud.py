# {"id":"780392644007","server":"api.zhiyun360.com","key":"dnsGB3p0dQAFBwN0RA1ABw0DDgw"}
# wss://api.zhiyun360.com:28090/

import json

import websockets
from loguru import logger


class WebSocketClient:
    def __init__(self):
        self.url = None
        self.websocket = None
        self.authorization = {
            "method": "authenticate",
            "uid": "780392644007",
            "key": "dnsGB3p0dQAFBwN0RA1ABw0DDgw"
        }

    async def connect(self, url: str):
        self.url = url
        self.websocket = await websockets.connect(self.url)
        await self.send_data(self.authorization)
        logger.success("Connected!")

    async def send_data(self, data):
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
            except websockets.exceptions.ConnectionClosedError:
                logger.critical("Connection Lost!")
                await self.connect(self.url)

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.success("Connection closed!")


client = WebSocketClient()

