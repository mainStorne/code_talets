from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from redis.asyncio import Redis
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import UserExistsGlobalDependency

from backend.web import TelegramData

students_route = APIRouter(prefix='/students', dependencies=([Depends(UserExistsGlobalDependency())]))

BASE_PATH = Path(__file__).parent.parent
templates = Jinja2Templates(str(BASE_PATH / 'templates'))





async def student_profile(request: Request,
                          telegram_data: TelegramData,
                          redis: Redis,
                          repo: RequestRepo):
    pass


# @students_profile.post('/profile/')
# async def user_profile(request: Request,
#                    telegram_data: TelegramData = Depends(get_telegram_data),
#                    role: str = Depends(get_user_role),
#                    redis: Redis = Depends(get_redis),
#                    repo: RequestRepo = Depends(get_repo)):
    # elif role == UserRolesEnum.student:
    #     pass
    # else:
    #     return Response(status_code=500)
