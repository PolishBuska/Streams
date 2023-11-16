from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     )

from app.models import User
from app.auth.jwt_handler import AuthProvider
from app.songs.repository import SongRepository

router = APIRouter(
    prefix='/song',
    tags=['songs']
)


@router.get('/all')
async def get_songs(limit: int = 10,
                    offset: int = 0,
                    search: Optional[str] = ""):
    db_adapter = SongRepository()
    result = await db_adapter.get_songs(limit=limit,
                                        offset=offset,
                                        search=search)
    return result


@router.get('/{song_id}')
async def get_song_by_id(song_id: int):
    db_adapter = SongRepository()
    result = await db_adapter.find_one(song_id)
    return result

