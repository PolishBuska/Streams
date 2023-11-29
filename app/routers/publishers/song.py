from typing import Optional, List

from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Depends,
                     )

from app.models import User, Song
from app.songs.service import SongService
from app.core.auth.jwt_handler import AuthProvider
from app.schemas.song import SongCreate, ReturnSongInfo
from app.songs.repository import SongRepository
from app.utils.generic_repo import get_repository

router = APIRouter(
    prefix='/publisher',
    tags=['publishers']
)


@router.post('/create')
async def create_song(song_info: SongCreate = Depends(),
                      file: UploadFile = File(...),
                      current_user: User = Depends(AuthProvider().get_current_user),
                      repo=Depends(get_repository(model=Song, repo=SongRepository))):
    song_manager_service = SongService(file=file,
                                       song_info=song_info,
                                       author_id=current_user.id,
                                       repo=repo)
    result = await song_manager_service.upload_song()
    return result


@router.get('/me', response_model=List[ReturnSongInfo])
async def get_song_by_user(current_user: User = Depends(AuthProvider().get_current_user),
                           limit: int = 10,
                           offset: int = 0,
                           search: Optional[str] = "",
                           repo=Depends(get_repository(model=Song, repo=SongRepository)),
                           ):
    result = await repo.get_songs_by_user(user_id=current_user.id,
                                          limit=limit,
                                          offset=offset,
                                          search=search)
    return result
