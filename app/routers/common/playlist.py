from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.playlists.repository import PlaylistRepository
from app.models import Playlist
from app.schemas.playlist import ReturnPlaylist
from app.schemas.song import PlSongs

from app.playlists.service import PlaylistService
from app.utils.exceptions import NotFound
from app.utils.generic_repo import get_repository

router = APIRouter(
    tags=['commons'],
    prefix="/common/pl",
                   )


@router.get('/', response_model=List[ReturnPlaylist])
async def find_playlists(
                         limit: int = 10,
                         offset: int = 0,
                         search: Optional[str] = "",
                         repo=Depends(get_repository(model=Playlist, repo=PlaylistRepository))
):
    pl = await repo.find_one_pl(
                                search=search,
                                limit=limit,
                                offset=offset)
    return pl


@router.get('/{pl_id}', response_model=List[PlSongs])
async def find_pl_related_songs(pl_id: int,
                                repo=Depends(get_repository(model=Playlist, repo=PlaylistRepository))):

    try:
        res = await PlaylistService.find_pl_related_songs(repo=repo,
                                                          pl_id=pl_id)
        return res

    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
