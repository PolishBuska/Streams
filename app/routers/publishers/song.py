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

router = APIRouter(
    prefix='/publisher',
    tags=['publishers']
)


@router.post('/create')
async def create_song(song_info: SongCreate = Depends(),
                      file: UploadFile = File(...),
                      current_user: User = Depends(AuthProvider().get_current_user)):
    song_manager_service = SongService(file=file,
                                       song_info=song_info,
                                       author_id=current_user.id)
    result = await song_manager_service.upload_song()
    return result


@router.get('/me', response_model=List[ReturnSongInfo])
async def get_song_by_user(current_user: User = Depends(AuthProvider().get_current_user),
                           limit: int = 10,
                           offset: int = 0,
                           search: Optional[str] = "",
                           ):
    db_adapter = SongRepository(model=Song)
    result = await db_adapter.get_songs_by_user(user_id=current_user.id,
                                                limit=limit,
                                                offset=offset,
                                                search=search)
    return result
