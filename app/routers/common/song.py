from typing import Optional, List

from fastapi import APIRouter, Depends

from app.models import Song
from app.songs.repository import SongRepository
from app.schemas.song import ReturnSongInfo
from app.utils.generic_repo import get_repository

router = APIRouter(
    tags=['commons'],
    prefix="/common/s",
                   )


@router.get('/all', response_model=List[ReturnSongInfo])
async def get_songs(limit: int = 10,
                    offset: int = 0,
                    search: Optional[str] = "",
                    repo=Depends(get_repository(model=Song, repo=SongRepository))):
    result = await repo.get_songs(limit=limit,
                                  offset=offset,
                                  search=search)
    return result


@router.get('/{song_id}', response_model=ReturnSongInfo)
async def get_song_by_id(song_id: int,
                         repo=Depends(get_repository(model=Song, repo=SongRepository))):
    result = await repo.find_one(pk=song_id)
    return result

