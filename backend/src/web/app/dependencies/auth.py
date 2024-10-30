from fastapi import Depends
from ..managers.user import UserManager
from sqlalchemy.ext.asyncio import AsyncSession
from .session import get_session
from ..db.models.users import User

from ..db.adapters.users import UserAdapter

async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield UserAdapter(session, User)


async def get_user_manager(user_db: UserAdapter = Depends(get_user_db)):
    yield UserManager(user_db)
