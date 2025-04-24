import asyncio
import os
from datetime import datetime

import uvicorn
from loguru import logger
from contextlib import asynccontextmanager

from api import app
from api.ext import websocket_background_task, global_ws_client
from core.zxcloud import create_client

# 创建日志目录
data_dir = "data"
log_dir = os.path.join(data_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"server_{datetime.now().strftime('%Y%m%d')}.log")
logger.add(
    log_filename,
    rotation="10 MB",  # 当日志文件达到10MB时轮转
    retention="30 days",  # 保留30天的日志
    compression="zip",  # 压缩旧日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    encoding="utf-8",
)


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
    uvicorn.run("api:app", host="0.0.0.0", port=10086, workers=2)
