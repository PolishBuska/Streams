from app.utils.hasher import SongHasher
from app.songs.repository import SongRepository


class FileService:
    def __init__(self, file, path, title, desc, author_id):
        self.file = file
        self.path = path
        self.title = title
        self.desc = desc
        self.author_id = author_id

    async def upload_song(self):
        try:
            file_manager = SongHasher(path=self.path,
                                      file=self.file,
                                      formats=["mp3", "wav"])
            file_data = await file_manager.hash_filename()
            db_song_manager = SongRepository()
            song_data = {"title": self.title,
                         "description": self.desc,
                         "filename": file_data.file_name,
                         "link": file_data.link}
            response = await db_song_manager.add_one(data=song_data)
            return response
        except Exception as e:
            raise e
