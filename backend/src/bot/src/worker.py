from .storage.cache.redis_client import RedisClient
import logging
from .conf import connection_pool, async_session_maker, bot, settings
from contextlib import asynccontextmanager
from .messages import UserCreateMessage
from .storage.db.adapters.base import BaseAdapter
from .storage.db.models.users import User
from pydantic import ValidationError
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo
from .conf import async_session_maker
from .storage.db.models.users import User, UserResume
from sqlalchemy import select


class Worker:
    async def handle_cases(self, message: UserCreateMessage):
        async with async_session_maker() as session:
            # stmt = select(User).join(UserResume, User.id == UserResume.user_id).where(User.id == message.user_id)
            admin = select(User).where(User.is_superuser==True)
            admin = await session.scalar(admin)

        builder = InlineKeyboardBuilder()
        builder.button(text='Отправьте тестовое задание для кандидата', web_app=WebAppInfo(url=f'{settings.DOMAIN_URL}/signup'))
        builder.adjust(1)

        await bot.send_message(admin.id, text=message.text, reply_markup=builder.as_markup())
        # async with async_session_maker() as session:

    async def __call__(self, *args, **kwargs):
        # maybe create ping
        async with RedisClient.from_pool(connection_pool) as redis:
            async for key, payload in redis.listen_for_stream():
                logging.info(f'recieved {key, payload}')
                if key == 'users.create':
                    try:
                        message = UserCreateMessage(**payload)
                        await self.handle_cases(message)
                    except ValidationError as e:
                        logging.error(exc_info=e, msg='Error in worker')
