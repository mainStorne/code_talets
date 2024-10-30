from sys import prefix

from fastapi import APIRouter
from .endpoints.register import r

api = APIRouter()
api.include_router(r, prefix='/users', tags=['users'])
