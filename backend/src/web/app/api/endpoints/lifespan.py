from fastapi import APIRouter, Depends
from ...schemas.lifespan import BaseUser, ReadUser
from fastapi_sqlalchemy_toolkit import ModelManager
from ...dependencies.redis import get_redis
from ...dependencies.session import get_session
from ...dependencies.telegram_validation import get_telegram_data
from ...schemas.telegram_data import TelegramData
from ...storage.db.adapters.base import BaseAdapter
from ...storage.db.models.users import User

r = APIRouter()
m = ModelManager(User)


@r.post('/register', response_model=ReadUser)
async def lifespan1(user: BaseUser, session=Depends(get_session), telegram: TelegramData = Depends(get_telegram_data)):
    return await m.create(session, ReadUser(**user.model_dump(), id=telegram.user.id))
