from .settings import settings
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot

SECRET = settings.JWT_PRIVATE_KEY
bot = Bot(settings.TELEGRAM_TOKEN)

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
connection_pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

