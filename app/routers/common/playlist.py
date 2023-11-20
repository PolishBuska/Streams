from typing import Optional, List

from fastapi import APIRouter

from app.playlists.repository import PlaylistRepository
from app.models import Playlist, PlaylistToSong
from app.schemas.playlist import ReturnPlaylist
from app.schemas.song import PlSongs

from app.playlists.service import PlaylistService

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


@router.get('/{pl_id}', response_model=List[PlSongs])
async def find_pl_related_songs(pl_id: int):
    res = await PlaylistService.find_pl_related_songs(repo=PlaylistRepository(model=PlaylistToSong),
                                                      pl_id=pl_id)
    return res
