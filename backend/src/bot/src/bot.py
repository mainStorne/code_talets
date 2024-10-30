import asyncio
from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from .handlers import start
from .middlewares.database import DatabaseMiddleware
from .settings import settings
from .conf import async_session_maker


async def main():

    # await create_tables(engine)

    bot = Bot(settings.TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.start_router)

    dp.update.outer_middleware(DatabaseMiddleware(async_session_maker))

    setup_dialogs(dp)


    await dp.start_polling(bot)


