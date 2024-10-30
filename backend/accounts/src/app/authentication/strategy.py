from fastapi_users import models
from fastapi_users.authentication.strategy.jwt import JWTStrategy
from fastapi_users.jwt import generate_jwt
from redis.asyncio import Redis

from ..db.models.users import User
from contextlib import asynccontextmanager
from ..dependencies.redis import get_redis


class Strategy(JWTStrategy):

    async def write_token(self, user: User) -> str:
        data = {"sub": str(user.id), "aud": self.token_audience, 'role': user.role.name if user.role else None,
                "superuser": user.is_superuser}
        token = generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )

        return token
