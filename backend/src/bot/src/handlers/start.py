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
from ..storage.db.models.users import User, UserResume
from ..storage.db.models.questions import Speciality

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import URLInputFile, CallbackQuery
from aiogram import F
from sqlalchemy import select
from ..storage.db.models.users import User
from aiogram.utils.markdown import hbold
from sqlalchemy.orm import joinedload

start_router = Router()


@start_router.message(CommandStart(), AdminFilter())
async def cmd_start_already_have_user(message: Message, user: User):
    # TODO create command list
    await message.answer(
        text='Здравствуйте админ! Google docs для просмотра пользователей:\n\n'
             'https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0\n\n'
    )


@start_router.message(Command('contacts'), AdminFilter())
async def contact(message: Message, user: User):
    builder = InlineKeyboardBuilder()
    names = ['хороший кандидат', 'отличный', 'не подходит', 'неизвестно']
    for name in names:
        builder.row(
            InlineKeyboardButton(
                text=name.title(),
                callback_data=f'user_{name}'
            )
        )

    builder.adjust(3)
    await message.answer('Контакты:', reply_markup=builder.as_markup())


@start_router.callback_query(lambda x: x.data.startswith('user_'))
async def get_cantacts(callback_query: CallbackQuery):
    await callback_query.answer()
    name = callback_query.data.replace('user_', '')
    if name == 'неизвестно':
        name = None
    async with async_session_maker() as session:
        stmt = select(User).where(User.status == name).where(User.is_superuser == False).options(
            joinedload(User.resume))
        users = (await session.scalars(stmt)).unique().all()
        logging.info(f'users - {users}')
    for user in users:
        text = \
            f"ФИО: {user.last_name} {user.first_name} {user.middle_name}\n" + \
            f"Опыт работы: {user.work_experience}\n" + \
            f"Возраст: {user.age}\n" + \
            f"Номер телефона: {user.phone_number}\n\n"
        doc = URLInputFile(settings.DOMAIN_URL + '' + user.resume.resume_url, filename='Резюме')
        await callback_query.bot.send_message(callback_query.from_user.id,
                                              text=text,
                                              )
        await callback_query.bot.send_document(callback_query.from_user.id, doc)

    logging.info('get contacts')



@start_router.callback_query(lambda x: x.data.startswith('spec_'))
async def proftest(callback_query: CallbackQuery):
    await callback_query.answer()
    spec_id = int(callback_query.data.replace('spec_', ''))
    async with async_session_maker() as session:
        spec = await session.get(Speciality, spec_id)
    text = spec.text + '\nДополнительные материалы:\n' + "\n".join([url for url in spec.urls.split(';')])
    logging.info('send proftest')
    await callback_query.bot.send_message(callback_query.from_user.id,
                                          text=text,
                                          )


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
