from typing import Optional, List

from fastapi import APIRouter

from app.playlists.repository import PlaylistRepository
from app.models import Playlist
from app.schemas.playlist import ReturnPlaylist

router = APIRouter(
    tags=['commons'],
    prefix="/common/pl",
                   )


@router.get('/', response_model=List[ReturnPlaylist])
async def find_playlists(
                         limit: int = 10,
                         offset: int = 0,
                         search: Optional[str] = ""):

    repo = PlaylistRepository(model=Playlist)
    pl = await repo.find_one_pl(
                                search=search,
                                limit=limit,
                                offset=offset)
    return pl
