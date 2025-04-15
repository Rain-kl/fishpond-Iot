import asyncio

from core.parser import parse_zx_response
from core.zxcloud import client


async def main():
    await client.connect("wss://api.zhiyun360.com:28090/")
    while True:
        response = await client.receive_message()
        parse_zx_response(response)

        print(response)


if __name__ == '__main__':
    asyncio.run(main())
