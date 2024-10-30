from aiogram.filters import BaseFilter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_sqlalchemy_toolkit import ModelManager
from ..storage.db.models import User


class HaveUserFilter(BaseFilter):

    async def __call__(self, message, session: AsyncSession):
        # m = ModelManager(User)
        # return await m.get(session, id=message.from_user.id)
        return None


class AdminFilter(HaveUserFilter):
    async def __call__(self, message, session: AsyncSession):
        user: User = await super.__call__(message, session)
        return user if user.is_superuser else None
