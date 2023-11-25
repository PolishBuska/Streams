from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     )

from app.models import User, LikedSongs
from app.core.auth.jwt_handler import AuthProvider
from app.playlists.personal import PersonalPlaylist

router = APIRouter(
    prefix='/listener/me',
    tags=['listeners']
)


@router.get('/personal_playlist')
async def get_liked_songs_by_user(current_user: User = Depends(AuthProvider().get_current_user),
                                  limit: int = 10,
                                  offset: int = 0,
                                  search: Optional[str] = ""
                                  ):
    raise NotImplementedError


@router.post('/{song_id}')
async def like_song(song_id: int,
                    current_user: User = Depends(AuthProvider().get_current_user)):
    service = PersonalPlaylist(model=LikedSongs)
    res = await service.add_to_personal_playlist(data={'song_id': song_id,
                                                 'user_id': current_user.id})
    return res


@router.get('/{song_id}/personal_playlist')
async def get_liked_song_by_id(song_id: int):
    raise NotImplementedError
