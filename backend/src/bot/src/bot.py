import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from .handlers import start
from .middlewares.database import DatabaseMiddleware
from .settings import settings
from .conf import async_session_maker, bot
from .worker import Worker
import logging



async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_routers(start.start_router)

    dp.update.outer_middleware(DatabaseMiddleware(async_session_maker))

    setup_dialogs(dp)
    worker = Worker()
    task = asyncio.create_task(worker())
    await dp.start_polling(bot)


