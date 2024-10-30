from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from ..buttons.inline import main_menu
from ..filters.user_filter import HaveUserFilter, AdminFilter
from ..settings import settings
from ..storage.db.models.users import User

start_router = Router()


# @start_router.message(CommandStart(), AdminFilter())
# async def cmd_start_already_have_user(message: Message, user: User):
#     # TODO create command list
#     await message.answer(
#         text='Здравствуйте админ! Google docs для просмотра пользователей: '
#     )
#




@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Здравствуйте! Для вашей регистрации пожалуйства нажмите 👇',
        reply_markup=main_menu(settings.DOMAIN_URL)
    )





