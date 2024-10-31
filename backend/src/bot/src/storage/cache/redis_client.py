from typing import Literal, AsyncGenerator
from ..db.models.users import User
from redis.asyncio import Redis


class RedisClient(Redis):
    service = 'm1m'

    async def broadcast_user_cud_stream(self, user: User, action: Literal['create', 'update', 'delete']):
        await self.xadd(f'{self.service}.{action}', {'user_id': user.id})

    async def listen_for_stream(self) -> AsyncGenerator[str, dict]:
        ids = {'user.action': '$', 'user.resumes': '$'}
        while True:
            response = await self.xread(ids, count=1, block=0)
            key, messages = response[0]
            last_id, payload = messages[0]
            ids[key] = last_id
            yield key, payload
