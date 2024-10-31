import asyncio
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.api import api
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi_pagination import add_pagination
from .worker import Worker
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app):
    logging.info('nice')
    worker = Worker()
    task = asyncio.create_task(worker())

    yield
    task.cancel()


app = FastAPI(root_path='/api', lifespan=lifespan)
app.include_router(api)
add_pagination(app)