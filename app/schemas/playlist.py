from typing import Annotated

from pydantic import BaseModel, constr, ConfigDict
from pydantic.types import datetime


class PlaylistBase(BaseModel):
    title: Annotated[str, constr(max_length=25)]
    description: Annotated[str, constr(max_length=200, min_length=5)]
    model_config = ConfigDict(extra='ignore',
                              from_attributes=True)


class CreatePlaylist(PlaylistBase):
    pass


class ReturnPlaylist(PlaylistBase):
    author_id: int
    id: int
    created_at: datetime
    model_config = ConfigDict(extra='ignore',
                              from_attributes=True)


class SongToPlaylist(BaseModel):
    song_id: int
    playlist_id: int
    model_config = ConfigDict(extra='ignore',
                              from_attributes=True)
