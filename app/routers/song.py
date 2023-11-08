from typing import Optional

from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Depends)

from app.models import User
from app.services.file import FileService
from app.users.auth import AuthProvider
from app.schemas.song import SongBase
from app.songs.repository import SongRepository

router = APIRouter(
    prefix='/song',
)


@router.post('/create')
async def create_song(song_info: SongBase,
                      file: UploadFile = File(...),
                      current_user: User = Depends(AuthProvider().get_current_user)):
    song_manager_service = FileService(file=file,
                                       title=song_info.title,
                                       path="app/static/",
                                       desc=song_info.description,
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


@router.get('/{song_id}')
async def get_song_by_id(song_id: int):
    db_adapter = SongRepository()
    result = await db_adapter.find_one(song_id)
    return result



