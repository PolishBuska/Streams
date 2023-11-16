from typing import Optional, Annotated

from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Depends,
                     Body)

from app.models import User
from app.songs.service import SongService
from app.auth.jwt_handler import AuthProvider
from app.schemas.song import SongCreate
from app.songs.repository import SongRepository

router = APIRouter(
    prefix='/song',
    tags=['songs']
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


@router.get('/all')
async def get_songs(limit: int = 10,
                    offset: int = 0,
                    search: Optional[str] = ""):
    db_adapter = SongRepository()
    result = await db_adapter.get_songs(limit=limit,
                                        offset=offset,
                                        search=search)
    return result


@router.get('/me')
async def get_song_by_user(current_user: User = Depends(AuthProvider().get_current_user),
                           limit: int = 10,
                           offset: int = 0,
                           search: Optional[str] = ""
                           ):
    db_adapter = SongRepository()
    result = await db_adapter.get_songs_by_user(user_id=current_user.id,
                                                limit=limit,
                                                offset=offset,
                                                search=search)
    return result


@router.get('/{song_id}')
async def get_song_by_id(song_id: int):
    db_adapter = SongRepository()
    result = await db_adapter.find_one(song_id)
    return result
