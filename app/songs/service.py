from app.utils.hashers.hasher import Hasher
from app.songs.repository import SongRepository
from app.songs.exceptions import SongError


class SongService:
    def __init__(self, file,
                 song_info,
                 author_id):
        self.file = file
        self.song_info = song_info
        self.author_id = author_id
        self.path = "app/static/",

    async def upload_song(self):
        try:
            file_manager = Hasher(path=self.path,
                                  file=self.file,
                                  formats=["mp3", "wav"])
            file_data = await file_manager.hash_filename()
            db_song_manager = SongRepository()
            song_data = {"title": self.song_info.title,
                         "description": self.song_info.desc,
                         "filename": file_data.filename,
                         "link": str(file_data.url),
                         "author_id": self.author_id}
            response = await db_song_manager.add_one(data=song_data)
            return response
        except Exception as e:
            raise SongError from e
