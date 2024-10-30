from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import session_pool, connection_pool
# from contextlib import asynccontextmanager, AsyncExitStack
from backend.infrastructure.database.repository.redis_client import RedisClient
# from backend.web.dependencies.redis import get_redis


async def get_repo() -> RequestRepo:
    async with RedisClient(connection_pool=connection_pool) as redis:
        async with session_pool() as session:
            yield RequestRepo(session, redis)

    # TODO handle this because if this execute not in dependency then connection remained available!
    # print('hello')