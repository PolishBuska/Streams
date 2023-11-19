from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.jwt_handler import AuthProvider
from app.playlists.service import PlaylistService
from app.schemas.playlist import CreatePlaylist, ReturnPlaylist
from app.models import Playlist, User
from app.playlists.repository import PlaylistRepository
from app.playlists.exceptions import PlaylistAlreadyExist

router = APIRouter(
    prefix='/director',
    tags=['director']
)


@router.post("/common_playlist", response_model=ReturnPlaylist)
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
