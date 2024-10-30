from typing import Type

from fastapi import APIRouter
from fastapi_users import FastAPIUsers as APIUsers, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from ..db.models.users import User
from .strategy import Strategy
from ..dependencies.auth import get_user_manager
from ..conf import SECRET
from ..api.endpoints.users import get_users_router
from ..api.endpoints.register import get_register_router
from ..dependencies.session import get_session

def get_strategy():
    return Strategy(SECRET, lifetime_seconds=6000)

transport = BearerTransport(tokenUrl='auth/jwt/login')

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=get_strategy,
)


class FastAPIUsers(APIUsers[User, int]):

    def get_users_router(
        self,
        user_schema: Type[schemas.U],
        user_update_schema: Type[schemas.UU],
        requires_verification: bool = False,
    ) -> APIRouter:
        return get_users_router(
            self.get_user_manager,
            user_schema, user_update_schema,
            self.authenticator,
            get_session,
            User,
            requires_verification,
        )
    def get_register_router(
        self, user_schema: Type[schemas.U], user_create_schema: Type[schemas.UC]
    ) -> APIRouter:
        return get_register_router(
            self.get_user_manager,
            user_schema, user_create_schema,
        )


fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
