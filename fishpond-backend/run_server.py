import asyncio

import uvicorn
from loguru import logger
from contextlib import asynccontextmanager

from api import app
from api.ext import websocket_background_task,global_ws_client
from core.zxcloud import create_client

@asynccontextmanager
async def lifespan(app):
    # 启动时执行
    logger.info("WebSocket client starting...")
    ws_client = create_client()
    logger.info("创建新的 WebSocket 连接...")
    await ws_client.connect()
    logger.info("WebSocket 连接已建立")
    global_ws_client.set_client(ws_client)
    asyncio.create_task(websocket_background_task(ws_client))
    yield
    await ws_client.close()


# 使用新的生命周期管理方式替代on_event
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    # uvicorn.run("api:app", port=10086)
    uvicorn.run(app, port=10086)
