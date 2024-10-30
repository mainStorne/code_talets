from .settings import Settings
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



settings = Settings()
SECRET = settings.JWT_PRIVATE_KEY
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
connection_pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)