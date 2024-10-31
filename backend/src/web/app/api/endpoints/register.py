import logging
from http.client import responses
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Body, Response
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
from ...fastapi_crud_toolkit.openapi_responses import already_exist, no_content
from .users import r as r2

r = APIRouter()
m = UserManager(User)
auth = Authenticator()

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
    junior_text = 'У этого кандитата не достаточно опыта, предлогаю на должность junior'
    default_text = 'Ознакомьтесь с этим кондидатом:'
    try:
        if user.work_experience.strip().lower() == 'нет' or float(user.work_experience) <= 0.5:
            text = junior_text
        else:
            text = default_text
    except ValueError:
        text = default_text

    user_status = 'нет статуса' if user.status is None else user.status
    await redis.xadd('users.create', {**user.model_dump(exclude={'is_superuser', 'created_at', 'status', 'id'}),
                                      'created_at': user.created_at.timestamp(), 'telegram': link,
                                      'text': text,
                                      'send_to_admin': int(send_to_admin),
                                      'status': user_status,
                                      'id': telegram.user.id,  # type: ignore
                                      })
    return response


@r.post('/upload', response_model=ResumeRead)
async def upload(file: UploadFile = File(),
                 session=Depends(get_session),
                 user: User = Depends(get_current_user()),
                 ):
    resume: UserResume = await m.get_and_save_file(session, {'user_id': user.id}, UserResume, 'resume_url', file)
    return resume
