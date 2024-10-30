from ..db.adapters.redis_client import RedisClient
from ..conf import connection_pool


async def get_redis():
    r = RedisClient(connection_pool=connection_pool)
    async with r:
        yield r
