from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth.jwt_handler import AuthProvider
from app.playlists.service import PlaylistService
from app.schemas.playlist import (CreatePlaylist,
                                  ReturnPlaylist,
                                  SongToPlaylist,
                                  )
from app.models import (Playlist,
                        User,
                        PlaylistToSong)
from app.playlists.repository import PlaylistRepository
from app.playlists.exceptions import (PlaylistAlreadyExist,
                                      M2MRelationExists)

router = APIRouter(
    prefix='/director',
    tags=['director']
)


@router.post("/pl/new", response_model=ReturnPlaylist)
async def create_common_playlist(pl_info: CreatePlaylist,
                                 current_user: User = Depends(AuthProvider().get_current_user)):
    try:
        service = PlaylistService(repo=PlaylistRepository(model=Playlist),
                                  info=pl_info)
        pl = await service.create_playlist(author_id=current_user.id)
        return pl
    except PlaylistAlreadyExist as pae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exist") from pae
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Unavailable") from e


@router.post("/pl", response_model=SongToPlaylist)
async def add_m2m_s_pl(s_pl_info: SongToPlaylist,
                       current_user: User = Depends(AuthProvider().get_current_user)):
    try:
        service = PlaylistService(repo=PlaylistRepository(model=PlaylistToSong),
                                  info=s_pl_info)
        pl = await service.subscribe_s_to_p()
        return pl
    except M2MRelationExists as m2m:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exist") from m2m
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Unavailable") from e
