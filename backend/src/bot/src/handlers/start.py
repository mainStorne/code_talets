import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from ..buttons.inline import main_menu
from ..filters.user_filter import HaveUserFilter, AdminFilter
from ..settings import settings
from ..conf import connection_pool, async_session_maker
from ..storage.db.adapters.redis_client import RedisClient
from ..storage.db.adapters.base import BaseAdapter
from ..storage.db.models.users import User
from ..storage.db.models.questions import Speciality
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import URLInputFile, CallbackQuery
from aiogram import F
from aiogram.utils.markdown import hbold

start_router = Router()


@start_router.message(CommandStart(), AdminFilter())
async def cmd_start_already_have_user(message: Message, user: User):
    # TODO create command list
    await message.answer(
        text='Здравствуйте админ! Google docs для просмотра пользователей:\n\n'
             'https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0\n\n'
    )


@start_router.callback_query(F.data.start_with('spec_'))
async def proftest(callback_query: CallbackQuery):
    await callback_query.answer()
    spec_id = int(callback_query.data.replace('spec_', ''))
    async with async_session_maker() as session:
        spec = await session.get(Speciality, spec_id)
    text = spec.text + '\nДополнительные материалы:\n' + "\n".join([hbold(url) for url in spec.urls.split(';')])
    logging.info('send proftest')
    await callback_query.bot.send_message(callback_query.from_user.id,
                                          text=text)


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    async with RedisClient(connection_pool=connection_pool) as redis:
        await redis.xadd('users.ping', {'id': message.from_user.id})
    await message.answer(
        text='Здравствуйте! Для вашей регистрации пожалуйста нажмите 👇',
        reply_markup=main_menu(settings.DOMAIN_URL)
    )


@start_router.message(Command('view_table'))
async def view_table(message: Message):
    await message.answer(
        text='https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0')
    # doc = URLInputFile('https://musical-pheasant-major.ngrok-free.app/staticfiles/cecc0c75-18ee-4fc6-b8ab-e56fc49bd5b5prakt_rabot_mdk_04.02_090207.pdf')
    # await message.bot.send_document(message.from_user.id, doc)
