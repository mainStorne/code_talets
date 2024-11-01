import asyncio

from .storage.cache.redis_client import RedisClient
import logging
from .conf import connection_pool, async_session_maker, bot, settings
from contextlib import asynccontextmanager
from .messages import UserCreateMessage, CaseAnswer, CaseRead
from .storage.db.adapters.base import BaseAdapter
from .storage.db.models.users import User
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo
from .conf import async_session_maker, settings
from .storage.db.models.users import User, UserResume
from sqlalchemy import select
from .buttons.inline import main_menu
import locale


class Worker:
    async def handle_create(self, message: UserCreateMessage):
        async with async_session_maker() as session:
            admin = select(User).where(User.is_superuser == True)
            admins = await session.scalars(admin)
            logging.info(f'Admin recieve {type(admins)} {admins}')
            if not admins:
                return

        builder = InlineKeyboardBuilder()
        builder.button(text=f'Отправьте тестовое задание для кандидата!\n\n{message.text}',
                       web_app=WebAppInfo(url=f'{settings.DOMAIN_URL}/send_test/{message.id}/'))
        builder.adjust(1)
        for admin in admins:
            await bot.send_message(admin.id, text='Вам сообщение!', reply_markup=builder.as_markup())

    async def handle_case_create(self, message: CaseRead):
        logging.info(f'Admin recieve')
        builder = InlineKeyboardBuilder()
        answer_case_url = WebAppInfo(url=f'{settings.DOMAIN_URL}/send_answer/{message.id}/')
        builder.button(text=f'Задание',
                       web_app=answer_case_url)
        builder.adjust(1)
        await bot.send_message(message.executor_id,
                               text=f'Вам отправили тестовое задание!\n\n Выполните его до {message.exp_at.strftime('%d-%m-%Y')}👇',
                               reply_markup=builder.as_markup())

    async def handle_answer_case(self, message: CaseAnswer):
        logging.info(f'Admin recieve ')
        builder = InlineKeyboardBuilder()
        admin_answer_case_url = WebAppInfo(url=f'{settings.DOMAIN_URL}/get_full/{message.id}')
        builder.button(text=f'Задание',
                       web_app=admin_answer_case_url)
        builder.adjust(1)
        await bot.send_message(message.user_id, text='Посмотрите ответ на тестовое задание 👇',
                               reply_markup=builder.as_markup())

    async def pinger(self, user_id: int):
        while True:
            await asyncio.sleep(20)
            async with async_session_maker() as session:
                user = select(User).where(User.id == user_id)
                user = await session.scalar(user)
                if user is None:
                    await bot.send_message(user_id, text='Вы не заполнили данные! Повторите пожалуйста',
                                           reply_markup=main_menu(settings.DOMAIN_URL))
                else:
                    break
            await asyncio.sleep(86400)

    async def __call__(self, *args, **kwargs):
        logging.info('Start Bot Worker')

        # locale.setlocale(locale.LC_ALL, 'russian')
        async with RedisClient.from_pool(connection_pool) as redis:
            async for key, payload in redis.listen_for_stream(
                    ['users.create', 'users.cases.answer', 'users.cases.create',
                     'users.ping', 'users.proftest']):
                logging.info(f'recieved {key, payload}')
                try:
                    if key == 'users.create':
                        message = UserCreateMessage(**payload)
                        # if message.send_to_admin is False:
                        #     continue
                        logging.info(f'message file {key}, {message}')
                        await self.handle_create(message)
                    elif key == 'users.cases.answer':
                        message = CaseAnswer(**payload)
                        logging.info(f'message file {key, message}')
                        await self.handle_answer_case(message)
                    elif key == 'users.cases.create':
                        message = CaseRead(**payload)
                        logging.info(f'message file {key, message}')
                        await self.handle_case_create(message)
                    elif key == 'users.ping':
                        user_id = int(payload['id'])
                        await self.pinger(user_id)

                except Exception as e:
                    logging.error(exc_info=e, msg='Error in worker')
