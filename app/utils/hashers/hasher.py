import secrets
from typing import List, Tuple
import os

from fastapi import UploadFile

from app.schemas.file import FileBase
from app.songs.exceptions import FormatError
from app.utils.hashers.interface import HasherInterface


class Hasher(HasherInterface):
    def __init__(self, file: UploadFile,
                 path: Tuple[str],
                 formats: List[str]):
        self.file = file
        self.path = path
        self.formats = formats

    async def hash_filename(self):
        try:
            filename = self.file.filename
            extension = filename.split(".")[1]
            path = f"app/static/{extension}/"
            if extension not in self.formats:
                raise ValueError("wrong format") from Exception
            else:
                os.makedirs(path, exist_ok=True)
                token_name = secrets.token_hex(15) + "." + extension
                generated_name = path + token_name
                file_content = await self.file.read()
                with open(generated_name, "wb") as file:
                    file.write(file_content)
                return FileBase(url=generated_name,
                                filename=filename)
        except Exception as e:
            raise FormatError from e

