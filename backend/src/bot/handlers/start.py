from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from backend.bot.src.app.buttons.inline import main_menu
from backend.bot.src.app.filters.user_filter import HaveUserFilter

start_router = Router()


@start_router.message(CommandStart(), HaveUserFilter())
async def cmd_start_already_have_user(message: Message, user):
    # TODO create command list
    await message.answer(
        text='Вы уже зарегестированны, список комманд:...'
    )


@start_router.message(CommandStart(), ~HaveUserFilter())
async def cmd_start(message: Message):
    await message.answer(
        text='Здравствуйте! Для вашей регистрации пожалуйства нажмите 👇',
        reply_markup=main_menu('https://musical-pheasant-major.ngrok-free.app')
    )





