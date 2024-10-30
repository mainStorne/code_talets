from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import ValidationError
from redis.asyncio import Redis

from ...db.models import UserResume
from ...schemas.users import BaseUser, ReadUser
from ...dependencies.redis import get_redis
from ...dependencies.session import get_session
from ...dependencies.user import get_current_user
from ...dependencies.telegram_validation import get_telegram_data
from ...schemas.telegram_data import TelegramData
from ...storage.db.adapters.base import BaseAdapter
from fastapi.encoders import jsonable_encoder
from ...db.models.users import User
from ...managers.user import UserManager
from ...schemas.resumes import ResumeRead
from ...db.adapters.redis_client import RedisClient

r = APIRouter()
m = UserManager(User)


def checker(data: str = Form(...)):
    try:
        return BaseUser.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@r.post('/register', response_model=ReadUser)
async def register(user: BaseUser, session=Depends(get_session),
                   telegram: TelegramData = Depends(get_telegram_data),
                   redis: RedisClient = Depends(get_redis)
                   ):
    user = ReadUser(**user.model_dump(), id=telegram.user.id)
    response = await m.create(session, user)
    link = f'https://t.me/{telegram.user.username}'
    user_datatime = user.created_at

    await redis.xsend(telegram.user.id,
                      {'timestamp': user_datatime.timestamp(), 'telegram_link': link,
                       **user.model_dump(exclude={'created_at', 'is_superuser', 'work_experience', 'id'})})
    return response


@r.post('/upload', response_model=ResumeRead)
async def upload(file: UploadFile = File(),
                 session=Depends(get_session),
                 user: User = Depends(get_current_user),
                 ):
    resume: UserResume = await m.create_resume(session, user.id, file)
    return resume
