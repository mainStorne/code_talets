from sys import prefix

from fastapi import APIRouter
from .endpoints.lifespan import r

api = APIRouter()
api.include_router(r, prefix='/users', tags=['users'])
