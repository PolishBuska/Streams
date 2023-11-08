from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import song

app = FastAPI(
    title="Streaming platform",
    description="This service provides with my own tracks"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(song.router)


@app.get('/')
async def root():
    return "Hello world"


