from typing import Optional, List

from fastapi import APIRouter

from app.models import Song
from app.songs.repository import SongRepository
from app.schemas.song import ReturnSongInfo

router = APIRouter(
    tags=['commons'],
    prefix="/common/s",
                   )


@router.get('/all', response_model=List[ReturnSongInfo])
async def get_songs(limit: int = 10,
                    offset: int = 0,
                    search: Optional[str] = ""):
    db_adapter = SongRepository(model=Song)
    result = await db_adapter.get_songs(limit=limit,
                                        offset=offset,
                                        search=search)
    return result


@router.get('/{song_id}', response_model=ReturnSongInfo)
async def get_song_by_id(song_id: int):
    db_adapter = SongRepository(model=Song)
    result = await db_adapter.find_one(pk=song_id)
    return result

