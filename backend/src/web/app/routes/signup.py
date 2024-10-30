import base64
import datetime
import logging
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Form, Request, Depends, Response
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from redis.asyncio import Redis
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import smtp_message
from backend.web import get_redis
from backend.web import get_telegram_data
from backend.web import get_repo
from backend.web import get_role_id
from backend.web import get_photo_url_and_write_user_photo_on_static_file
from backend.web import settings
from web.app.schemas.telegram_data import TelegramData
from backend.web.src.app.utils import create_verification_code
from backend.web.src.app.utils import templates, BASE_PATH
from backend.web.src.app.utils.authorized_user_router import NonAuthorizedUserAPIRouter

signup_router = NonAuthorizedUserAPIRouter(prefix='/signup')

static_files = StaticFiles(directory=str(BASE_PATH / 'static'))


@signup_router.get('/')
async def signup(request: Request, telegram_data: TelegramData = Depends(get_telegram_data),
                 redis: Redis = Depends(get_redis)):
    if (await redis.hget(f'user_signup:{telegram_data.user.id}', 'user_id')) is not None:
        return templates.TemplateResponse(request=request, name='partials/signup/group.html')
    return templates.TemplateResponse(request=request, name='signup.html',
                                      context={'client_id': settings.oath2_yandex.client_id.get_secret_value()})


@signup_router.post('/')
async def post_signup(request: Request, code: Annotated[str, Form()],
                      telegram_data: TelegramData = Depends(get_telegram_data),
                      redis: Redis = Depends(get_redis)):
    logging.info(request)
    res = base64.b64encode(
        f'{settings.oath2_yandex.client_id.get_secret_value()}:{settings.oath2_yandex.client_secret.get_secret_value()}'.encode()).decode()
    async with ClientSession() as session:
        response = await session.post('https://oauth.yandex.ru/token',
                                      headers={
                                          'Content-Type': 'application/x-www-form-urlencoded',
                                          'Authorization': f'Basic {res}'},
                                      data={'grant_type': 'authorization_code',
                                            'code': code})
        res = await response.json()
        # check if this email is ranepa
        api_response = await session.get('https://login.yandex.ru/info', headers={
            'Authorization': f'OAuth {res["access_token"]}'})

        if api_response.status != 200:
            pass
        user_data = await api_response.json()
        for email in user_data['emails']:
            email: str
            if email.endswith('@ranepa.ru'):
                names = user_data['display_name'].split()
                if len(names) == 3:
                    for name in names:
                        if name != user_data['first_name'] and name != user_data['last_name']:
                            await redis.hset(f'user_signup:{telegram_data.user.id}',
                                             mapping={
                                                 'user_id': telegram_data.user.id,
                                                 'first_name': user_data['first_name'],
                                                 'last_name': user_data['last_name'],
                                                 'middle_name': name,
                                                 'email': email,
                                                 'photo_url': f'https://avatars.yandex.net/get-yapic/{user_data["default_avatar_id"]}'
                                             })
                else:
                    await redis.hset(f'user_signup:{telegram_data.user.id}',
                                     mapping={
                                         'user_id': telegram_data.user.id,
                                         'first_name': user_data['first_name'],
                                         'last_name': user_data['last_name'],
                                         'middle_name': None,
                                         'email': email,
                                         'photo_url': f'https://avatars.yandex.net/get-yapic/{user_data["default_avatar_id"]}'
                                     })

                return templates.TemplateResponse(request=request, name='partials/signup/group.html')

        else:
            return templates.TemplateResponse(request=request, name='signup.html',
                                              context={'client_id': settings.oath2_yandex.client_id.get_secret_value(),
                                                       'error': 'Ошибка! Неверно указанна почта!'})


@signup_router.get('/group')
async def choice_group(request: Request):
    return templates.TemplateResponse(request=request, name='partials/signup/group.html')


@signup_router.post('/group')
async def choice_group(request: Request, group_id: Annotated[int, Form()],
                       telegram_data: TelegramData = Depends(get_telegram_data),
                       repo: RequestRepo = Depends(get_repo)):
    user_data = await repo.redis.hgetall(f'user_signup:{telegram_data.user.id}')
    user_id = int(user_data.pop('user_id'))
    # This isn't possible, but I want to check it ...
    if telegram_data.user.id != user_id:
        return templates.TemplateResponse(request=request, name='signup.html',
                                          context={'client_id': settings.oath2_yandex.client_id.get_secret_value(),
                                                   'error': 'Ваша сессия истекла повторите снова'})

    await repo.student.create_student(user_id=user_id, **user_data, group_id=group_id)
    return templates.TemplateResponse(request, name='/messages/messages.html')


@signup_router.get('/email/')
async def enter_email(request: Request,
                      telegram_data: TelegramData = Depends(get_telegram_data),
                      redis: Redis = Depends(get_redis),
                      ):
    result = await redis.hget(f'user:{telegram_data.user.id}', 'email')
    return templates.TemplateResponse(request=request, name='partials/signup/enter-email.html',
                                      context={'email': result if result else ''})


@signup_router.post('/email/')
async def send_email(request: Request, email: Annotated[EmailStr, Form()],
                     telegram_data: TelegramData = Depends(get_telegram_data),
                     redis: Redis = Depends(get_redis),
                     repo: RequestRepo = Depends(get_repo)
                     ):
    """
    send email -> user received -> send redis expiration command for user_id and created verification code on 10 minutes
    and safe user email
    """
    if email.endswith('edu.ranepa.ru'):
        role = await repo.role.get_role_by_name('student')
        role_id = role.id
    elif email.endswith('ranepa.ru'):
        role = await repo.role.get_role_by_name('teacher')
        role_id = role.id
    else:
        return templates.TemplateResponse(request=request, name='partials/signup/enter-email.html',
                                          context={'error': 'Введите корпоративную почту!'})

    verification_code = create_verification_code()
    exp_key_name = f'code:{telegram_data.user.id}'
    exp_key_time = datetime.timedelta(minutes=10)
    user_hash = f'user:{telegram_data.user.id}'
    # TODO INFO TURN ON IN PROFUCTION
    await smtp_message.asend_email(receiver=email, verification_code=verification_code)
    res1 = await redis.set(exp_key_name, value=verification_code, ex=exp_key_time)
    result = await redis.hset(user_hash, key='email', value=email)
    exp_result = await redis.expire(user_hash, datetime.timedelta(hours=1))
    if exp_result is False:
        pass

    return templates.TemplateResponse(request=request, name='partials/signup/confirm-email.html',
                                      context={'expiration_min': exp_key_time, 'role_id': role_id})


@signup_router.post('/email/confirm/')
async def confirm_email(request: Request,
                        code: Annotated[str, Form()],
                        role_id: int = Depends(get_role_id),
                        telegram_data: TelegramData = Depends(get_telegram_data),
                        redis: Redis = Depends(get_redis),
                        repo: RequestRepo = Depends(get_repo)):
    verification_code = await redis.get(f'code:{telegram_data.user.id}')
    if verification_code is None:
        # verification code is expired!
        return templates.TemplateResponse(request=request, name='partials/signup/confirm-email.html',
                                          context={'error': 'Код подтверждения истёк!'})
    elif code != verification_code:
        return templates.TemplateResponse(request=request, name='partials/signup/confirm-email.html',
                                          context={'error': 'Код подтверждения не совпадает!'})

    role = await repo.role.get_role(role_id)
    if role.name == 'teacher':
        return templates.TemplateResponse(request=request, name='partials/signup/teacher-cred.html')
    elif role.name == 'student':
        return templates.TemplateResponse(request=request, name='partials/signup/student-cred.html')
    else:
        # Нет роли у пользователя
        return Response(status_code=400)


@signup_router.post('/teacher/finish/')
async def teacher_signup_finish(request: Request,
                                first_name: Annotated[str, Form()],
                                middle_name: Annotated[str, Form()],
                                last_name: Annotated[str, Form()],
                                telegram_data: TelegramData = Depends(get_telegram_data),
                                redis: Redis = Depends(get_redis),
                                repo: RequestRepo = Depends(get_repo)):
    photo_url = get_photo_url_and_write_user_photo_on_static_file(BASE_PATH, telegram_data.user.id)

    teacher = await redis.hgetall(f'user:{telegram_data.user.id}')

    teacher_email = teacher.get('email', None)
    if teacher_email is None:
        return templates.TemplateResponse(request=request, name='signup.html',
                                          context={'error': 'Истекло время ожидания, повторите регистрацию.'})

    await repo.teacher.create_teacher(user_id=telegram_data.user.id,
                                      first_name=first_name,
                                      last_name=last_name,
                                      photo_url=photo_url,
                                      email=teacher_email,
                                      middle_name=middle_name,
                                      )

    return templates.TemplateResponse(request, name='/messages/messages.html')


@signup_router.post('/student/finish/')
async def student_signup_finish(request: Request,
                                first_name: Annotated[str, Form()],
                                last_name: Annotated[str, Form()],
                                group_id: Annotated[int, Form()],
                                telegram_data: TelegramData = Depends(get_telegram_data),
                                redis: Redis = Depends(get_redis),
                                repo: RequestRepo = Depends(get_repo)):
    photo_url = get_photo_url_and_write_user_photo_on_static_file(BASE_PATH / 'static', telegram_data.user.id)

    student = await redis.hgetall(f'user:{telegram_data.user.id}')
    student_email = student.get('email', None)
    if student_email is None:
        return templates.TemplateResponse(request=request, name='signup.html',
                                          context={'error': 'Истекло время сессии, повторите регистрацию.'})

    await repo.student.create_student(user_id=telegram_data.user.id,
                                      first_name=first_name,
                                      last_name=last_name,
                                      middle_name=None,
                                      group_id=group_id,
                                      photo_url=photo_url,
                                      email=student_email,
                                      )

    return templates.TemplateResponse(request, name='/messages/messages.html')