from typing import Literal
from ..models.users import User

from redis.asyncio import Redis


class RedisClient(Redis):
    channel = 'accounts'

    async def broadcast_user_cud_actions(self, user: User, action: Literal['create', 'update', 'delete']):
        await self.xadd(f'{self.channel}.{action}',
                        {'user_id': user.id, 'email': user.email, 'is_active': int(user.is_active),
                         'is_superuser': int(user.is_superuser), 'is_verified': int(user.is_verified)})


    async def xsend(self,
                    data: dict[bytes | memoryview | str | int | float, bytes | memoryview | str | int | float]):
        await self.xadd(f'user.action', data)
