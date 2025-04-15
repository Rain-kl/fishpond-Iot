import asyncio

import uvicorn
from loguru import logger
from contextlib import asynccontextmanager

from api import app
from api.ext import ws_client, websocket_background_task


@asynccontextmanager
async def lifespan(app):
    # 启动时执行
    logger.info("WebSocket client starting...")
    task = asyncio.create_task(websocket_background_task())

    yield  # 服务运行期间

    # 关闭时执行
    if ws_client:
        await ws_client.close()


# 使用新的生命周期管理方式替代on_event
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run("api:app", port=10086, reload=True)
