# -*- coding:utf-8 -*-

import traceback
import logging

import aioredis

from tornado.options import options


class AsyncRedisClient(object):
    def __init__(self,loop=None):
        self.loop = loop

    async def init_pool(self, db=None):
        if db is None:
            _db = options.redis_db4
        else:
            _db = db
        uri = 'redis://{}:{}/{}'.format(
            options.redis_host,
            options.redis_port,
            _db
        )

        self.pool = await aioredis.create_pool(
            uri,
            password=options.redis_password,
            # encoding="utf-8",
            minsize=5, 
            maxsize=10,
            loop = self.loop,
        )
        super(AsyncRedisClient, self).__init__()

    async def execute(self, command, *args, **kwargs):
        try:
            async with self.pool.get() as conn:    
                retsult = await conn.execute(command, *args, **kwargs)
            return retsult
        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error("redis execute error: %s", e)
    
    async def get(self, key):
        return await self.execute('get', key)

    async def set(self, key, value):
        return await self.execute('set', key, value)

    async def setex(self, key, seconds, value):
        return await self.execute('setex', key, seconds, value)

    async def keys(self, key):
        return await self.execute('keys', key)

    async def hgetall(self, key):
        return await self.execute('hgetall', key)
    async def scan(self, key):
        return await self.execute('scan', key)


async def connect(loop, db=None):
    client = AsyncRedisClient(loop)
    await client.init_pool(db)
    return client