from typing import Optional, List

from fastapi import (HTTPException,
                     status,
                     APIRouter,
                     Depends,
                     )

from app.models import User, LikedSongs
from app.core.auth.jwt_handler import AuthProvider
from app.playlists.personal_p.repository import PersonalPlaylistRepository
from app.playlists.exceptions import LikeAlreadyExist
from app.schemas.song import ReturnSongInfo
from app.utils.generic_repo import get_repository

router = APIRouter(
    prefix='/listener/me',
    tags=['listeners']
)


@router.get('/personal_playlist', response_model=List[ReturnSongInfo])
async def get_liked_songs_by_user(current_user: User = Depends(AuthProvider().get_current_user),
                                  repo=Depends(get_repository(model=LikedSongs, repo=PersonalPlaylistRepository)),
                                  limit: int = 10,
                                  offset: int = 0,
                                  search: Optional[str] = ""
                                  ):
    res = await repo.get_liked_songs_by_user(user_id=current_user.id,
                                             search=search,
                                             offset=offset,
                                             limit=limit)
    return res


@router.post('/{song_id}')
async def like_song(song_id: int,
                    current_user: User = Depends(AuthProvider().get_current_user),
                    repo=Depends(get_repository(model=LikedSongs, repo=PersonalPlaylistRepository))):
    try:
        res = await repo.add_to_personal_playlist(
            data=
            {
                'song_id': song_id,
                'owner_id': current_user.id
            }
                                                  )
        return res
    except LikeAlreadyExist as lae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Like already exist") from lae


@router.get('/{song_id}/personal_playlist')
async def get_liked_song_by_id(song_id: int):
    raise NotImplementedError
