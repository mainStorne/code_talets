from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Body
from pydantic import ValidationError
from redis.asyncio import Redis

from ...db.models import UserResume
from ...schemas.users import BaseUser, ReadUser, UpdateUser
from ...dependencies.redis import get_redis
from ...dependencies.session import get_session
from ...dependencies.user import get_current_user
from ...dependencies.telegram_validation import get_telegram_data
from ...schemas.telegram_data import TelegramData
from ...db.models.users import User
from ...managers.user import UserManager
from ...schemas.resumes import ResumeRead
from ...db.adapters.redis_client import RedisClient
from ...conf import bot
from ...fastapi_crud_toolkit.crud import get_crud_router
from ...authenticator import Authenticator
from ...fastapi_crud_toolkit.openapi_responses import already_exist

r = APIRouter()
m = UserManager(User)
auth = Authenticator()

r2 = get_crud_router(m,
                     get_session,
                     ReadUser, BaseUser, UpdateUser,
                     auth)
r.include_router(r2)


# TODO поговорить с Никитов по поводу этого роутера
@r.post('/register', response_model=ReadUser, responses={**already_exist})
async def register(user: Annotated[BaseUser, Body(embed=True)],
                   send_to_admin: bool,
                   session=Depends(get_session),
                   telegram: TelegramData = Depends(get_telegram_data),
                   redis: RedisClient = Depends(get_redis)
                   ):
    user = ReadUser(**user.model_dump(), id=telegram.user.id)
    if await m.get(session, id=user.id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    response = await m.create(session, user)
    link = f'https://t.me/{telegram.user.username}'
    user_datatime = user.created_at
    if send_to_admin:
        admin = await m.get(session, is_superuser=True)
        junior_text = 'У этого кандитата не достаточно опыта, предлогаю на должность junior'
        default_text = 'Ознакомьтесь с этим кондидатом:'
        try:
            if user.work_experience.strip() == 'нет' or float(user.work_experience) <= 0.5:
                text = junior_text
            else:
                text = default_text
        except ValueError:
            text = default_text

        # await bot.send_message(response.id, )
    # await redis.xsend({'timestamp': user_datatime.timestamp(), 'telegram_link': link,
    #                    **user.model_dump(exclude={'is_superuser'})})
    return response


@r.post('/upload', response_model=ResumeRead)
async def upload(file: UploadFile = File(),
                 session=Depends(get_session),
                 user: User = Depends(get_current_user()),
                 ):
    resume: UserResume = await m.create_resume(session, user.id, file)
    return resume
