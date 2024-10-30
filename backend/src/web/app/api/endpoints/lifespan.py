from fastapi import APIRouter, Depends
from ...schemas.lifespan import Lifespan1
from ...dependencies.redis import get_redis

r = APIRouter()

@r.get('/start')
async def lifespan1(lifespan: Lifespan1):
    pass