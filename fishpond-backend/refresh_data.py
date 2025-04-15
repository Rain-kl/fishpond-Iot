import json
from typing import TypedDict

from core.zxcloud import client
import asyncio
from redis_mq import RedisSqliteSync


class ZXResponseModel(TypedDict):
    TYPE: str
    PN: str
    A0: str
    A4: str
    A5: str
    A6: str
    A7: str
    D1: str


async def main():
    await client.connect("wss://api.zhiyun360.com:28090/")
    redis = RedisSqliteSync(db_path="data.db")
    while True:
        response = await client.receive_message()
        data = json.loads(response)

        print(response)


if __name__ == '__main__':
    asyncio.run(main())
