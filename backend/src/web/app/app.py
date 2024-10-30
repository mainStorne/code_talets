from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.api import api
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(root_path='/api', lifespan=lifespan)
app.include_router(api)
add_pagination(app)