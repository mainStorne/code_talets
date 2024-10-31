import asyncio
from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from .handlers import start
from .middlewares.database import DatabaseMiddleware
from .settings import settings
from .conf import async_session_maker, connection_pool
from .storage.cache.redis_client import RedisClient

async def worker():
    # maybe create ping
    async with RedisClient.from_pool(connection_pool) as redis:
        async for key, payload in redis.listen_for_stream():
            if key == 'user.action':
                pass

async def main():

    bot = Bot(settings.TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.start_router)

    dp.update.outer_middleware(DatabaseMiddleware(async_session_maker))

    setup_dialogs(dp)

    await dp.start_polling(bot)


