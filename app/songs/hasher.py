import secrets
from typing import List

from fastapi import UploadFile

from app.schemas.song_file import SongFileSchema
from app.songs.exceptions import FormatError


class SongHasher:
    def __init__(self, file: UploadFile,
                 path: str,
                 formats: List[str]):
        self.file = file
        self.path = path
        self.formats = formats

    async def hash_filename(self):
        try:
            file_name = self.file.filename
            extension = file_name.split(".")[1]
            if extension not in self.formats:
                raise ValueError("wrong format")
            else:
                token_name = secrets.token_hex(15) + "." + extension
                generated_name = self.path + token_name
                file_content = await self.file.read()
                with open(generated_name, "wb") as file:
                    file.write(file_content)
                return SongFileSchema(link=generated_name,
                                      file_name=file_name)
        except Exception as e:
            raise FormatError from e
