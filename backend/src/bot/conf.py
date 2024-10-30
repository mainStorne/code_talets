import redis.asyncio as redis
from pathlib import Path
from backend.infrastructure.database.setup import create_session_pool, create_async_engine
from backend.infrastructure.settings import Settings

settings = Settings(_env_file=Path(r'C:\Users\bevzD\PycharmProjects\telegram_bot_mini_app_project\backend\.env'))
engine = create_async_engine(settings.db.sqlalchemy_url)
session_pool = create_session_pool(engine)


connection_pool = redis.ConnectionPool(host=settings.redis.host.get_secret_value(), port=settings.redis.port)

