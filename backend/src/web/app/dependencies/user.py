from fastapi import Depends, HTTPException, status
from .session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .telegram_validation import get_telegram_data
from ..schemas.telegram_data import TelegramData
from ..db.adapters.base import BaseAdapter
from ..db.models.users import User



async def get_current_user(session: AsyncSession = Depends(get_session),
                      tg_data: TelegramData = Depends(get_telegram_data)):
    user = await session.get(User, tg_data.user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

