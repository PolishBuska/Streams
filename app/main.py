from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import registration, login
from app.routers.common.song import router as common_s
from app.routers.common.playlist import router as common_pl
import app.routers.publishers.song as pub_s
import app.routers.directors.playlist as pl

app = FastAPI(
    title="Streaming platform",
    description="This service provides with my own tracks"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(registration.router)
app.include_router(login.router)
app.include_router(common_s)
app.include_router(common_pl)
app.include_router(pub_s.router)
app.include_router(pl.router)


@app.get('/')
async def root():
    return "Hello world"


