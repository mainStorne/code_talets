import asyncio
from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from backend.bot.src.app.handlers import start
from backend.bot.src.app.middlewares.database import DatabaseMiddleware
from backend.web import settings
from web.app.settings import settings
from backend.infrastructure.database.setup import create_session_pool, create_async_engine


async def main():
    engine = create_async_engine(settings.db.sqlalchemy_url)
    session_pool = create_session_pool(engine)

    # await create_tables(engine)

    bot = Bot(settings)
    dp = Dispatcher()
    dp.include_routers(start.start_router)

    dp.update.outer_middleware(DatabaseMiddleware(session_pool))

    setup_dialogs(dp)


    await dp.start_polling(bot)





if __name__ == '__main__':
    asyncio.run(main())
