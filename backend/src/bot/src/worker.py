from .storage.cache.redis_client import RedisClient
import logging
from .conf import connection_pool, async_session_maker, bot
from contextlib import asynccontextmanager
from .messages import ResumeMessage
from .storage.db.adapters.base import BaseAdapter
from .storage.db.models.users import User
from pydantic import ValidationError
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo


class Worker:
    async def handle_resume(self, message: ResumeMessage):
        builder = InlineKeyboardBuilder()
        builder.button(text='Не', web_app=WebAppInfo(url=f'{domain}/signup'))
        builder.button(text='Да', web_app=WebAppInfo(url='https://9w8x7mzf-5173.use.devtunnels.ms/send_request'))
        builder.adjust(1)
        builder.as_markup()
        await bot.send_message(message.user_id, text=message.text, reply_markup=)
        # async with async_session_maker() as session:




    async def __call__(self, *args, **kwargs):
        # maybe create ping
        async with RedisClient.from_pool(connection_pool) as redis:
            async for key, payload in redis.listen_for_stream():
                if key == 'user.resume':
                    try:
                        message = ResumeMessage(**payload)
                        await self.handle_resume(message)
                    except ValidationError as e:
                        logging.error(exc_info=e, msg='Error in worker')

