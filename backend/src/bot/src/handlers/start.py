from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from ..buttons.inline import main_menu
from ..filters.user_filter import HaveUserFilter, AdminFilter
from ..settings import settings
from ..storage.db.models.users import User
from aiogram.types import URLInputFile
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

@start_router.message(Command('view_table'))
async def view_table(message: Message):
    await message.answer(text='https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0')
    # doc = URLInputFile('https://musical-pheasant-major.ngrok-free.app/staticfiles/cecc0c75-18ee-4fc6-b8ab-e56fc49bd5b5prakt_rabot_mdk_04.02_090207.pdf')
    # await message.bot.send_document(message.from_user.id, doc)



