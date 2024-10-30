from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas
from ..conf import SECRET
from ..db.adapters.users import UserAdapter
from ..db.models.users import User
from contextlib import asynccontextmanager
from ..dependencies.redis import get_redis
from ..db.adapters.redis_client import RedisClient
from fastapi_users import exceptions
from fastapi_sqlalchemy_toolkit import ModelManager
from ..db.models.roles import Role
from ..schemas.users import UserCreate
from ..exceptions import RoleDoesntExist


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    user_db: UserAdapter

    async def create(
            self,
            user_create: UserCreate,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        role_manager = ModelManager(Role)
        role = await role_manager.get(self.user_db.session, id=user_dict.pop('role_id'))
        if role is None:
            raise RoleDoesntExist

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict, role)

        await self.on_after_register(created_user, request)

        return created_user


    async def on_after_register(
            self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        async with asynccontextmanager(get_redis)() as redis:
            redis: RedisClient
            await redis.broadcast_user_cud_actions(user, 'create')
