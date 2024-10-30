from fastapi import Depends
from typing import Optional
from backend.infrastructure.database.repository.request import RequestRepo
from backend.infrastructure.database.models.users import User
from .repository import get_repo
from backend.web import TelegramData
from backend.web import get_telegram_data


async def get_user(role: str | None = None, telegram_data: TelegramData = Depends(get_telegram_data),
                   repo: RequestRepo = Depends(get_repo)) -> Optional[User]:

    return await repo.user.get_user(telegram_data.user.id)



