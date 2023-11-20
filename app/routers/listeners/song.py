from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     )

from app.models import User
from app.auth.jwt_handler import AuthProvider

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
async def like_song(song_id: int):
    raise NotImplementedError


@router.get('/{song_id}/personal_playlist')
async def get_liked_song_by_id(song_id: int):
    raise NotImplementedError
