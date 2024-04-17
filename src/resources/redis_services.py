import os
from typing import Any

import redis.asyncio as aioredis
from redis.client import Redis as AioRedis


def redis_conn_string(host: str | None = None, db: int | None = None) -> str:
    if os.getenv("REDIS_DSN"):
        return os.getenv("REDIS_DSN")
    else:
        host = host or os.getenv("REDIS_HOST")
        db = db if db is not None else os.getenv("REDIS_DB")
        return f'redis://{host}:6379/{db}'


class Redis:

    def __init__(self):
        self.connection: AioRedis | None = None

    async def up(self, conn_string: str = None):
        self.connection = await aioredis.from_url(
            conn_string or redis_conn_string(),
            encoding='utf-8',
            decode_responses=True,
        )
        await self.connection.execute_command('PING')
        return self

    async def down(self):
        if self.connection:
            await self.connection.close()  # noqa
        return self

    async def _exec(self, *args):
        try:
            return await self.connection.execute_command(*args)
        except Exception as e:
            raise e

    async def set(self, key: str, value: Any, expire=0):
        params = ('set', key, value)
        if expire:
            params += ('ex', expire)
        return await self._exec(*params)

    async def get(self, key: str):
        return await self._exec('get', key)

    async def get_int(self, key: str) -> int | None:
        if value := await self.get(key):
            return int(value)

    async def delete(self, key: str, *args):
        return await self._exec('del', key, *args)

    async def expire(self, key: str, seconds: int):
        return await self._exec('expire', key, seconds)

    async def scan(self, match: str = '*') -> list[str]:
        """ Go-round all DB keys """
        keys_ = []
        async for key in self.connection.scan_iter(match=match):  # noqa
            keys_.append(key)
        return keys_

    async def remove_all(self, match: str = '*'):
        """ Remove all keys by pattern in a background process """
        keys_ = await self.scan(match)
        if keys_:
            await self._exec('unlink', *keys_)


redis = Redis()
