from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.api import api

from contextlib import asynccontextmanager
from .conf import engine
from .db.setup import create_db_and_tables
from pathlib import Path

@asynccontextmanager
async def lifespan(app):
    await create_db_and_tables(engine)
    yield


app = FastAPI(root_path='/api/accounts', lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")
app.include_router(api)