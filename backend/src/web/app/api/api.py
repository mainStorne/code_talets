from sys import prefix

from fastapi import APIRouter
from .endpoints import register, cases, quote

api = APIRouter()
api.include_router(register.r, prefix='/users', tags=['users'])
api.include_router(cases.r, prefix='/cases', tags=['cases'])
api.include_router(quote.r, prefix='/quote', tags=['quote'])

