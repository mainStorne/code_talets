from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from redis.asyncio import Redis
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import UserExistsGlobalDependency

from backend.web import TelegramData

teachers_route = APIRouter(prefix='/teachers', dependencies=([Depends(UserExistsGlobalDependency())]))

BASE_PATH = Path(__file__).parent.parent
templates = Jinja2Templates(str(BASE_PATH / 'templates'))




async def student_profile(request: Request,
                          telegram_data: TelegramData,
                          redis: Redis,
                          repo: RequestRepo):
    pass



