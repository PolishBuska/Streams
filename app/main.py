from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.routers import registration, login
from app.routers.common.song import router as common_s
from app.routers.common.playlist import router as common_pl
from app.routers.listeners.song import router as listener
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
#app.include_router(listener)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return "Hello world"


