from typing import Annotated,List
from pydantic import (BaseModel,
                      constr,
                      ConfigDict)

from app.schemas.file import FileBase


class SongBaseInfo(BaseModel):
    title: Annotated[str, constr(max_length=100)]
    description: Annotated[str, constr(max_length=25)]
    model_config = ConfigDict(extra='ignore',
                              from_attributes=True)


class SongCreate(SongBaseInfo):
    pass


class ReturnSongInfo(SongBaseInfo):
    id: int


class SongFileInfo(SongBaseInfo):
    id: int
    file: FileBase


class PlSongs(SongBaseInfo):
    id: int
    filename: str
    link: str