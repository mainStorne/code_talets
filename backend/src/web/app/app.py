from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.api import api
from contextlib import asynccontextmanager
from pathlib import Path

@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(root_path='/api', lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")
app.include_router(api)