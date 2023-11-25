from app.utils.hashers.hasher import Hasher
from app.songs.repository import SongRepository
from app.songs.exceptions import SongError
from app.models import Song
from app.core.config import settings


class SongService:
    def __init__(self, file,
                 song_info,
                 author_id):
        self.file = file
        self.song_info = song_info
        self.author_id = author_id
        self.path = settings.static,
        self.repo = SongRepository(model=Song)

    async def upload_song(self):
        try:
            file_manager = Hasher(path=self.path,
                                  file=self.file,
                                  formats=["mp3", "wav"])
            file_data = await file_manager.hash_filename()
            song_data = {"title": self.song_info.title,
                         "description": self.song_info.description,
                         "filename": file_data.filename,
                         "link": str(file_data.url),
                         "author_id": self.author_id}
            response = await self.repo.add_one(data=song_data)

            return response
        except Exception as e:
            raise SongError from e

