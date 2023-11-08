from typing import Annotated
from pydantic import BaseModel, constr, ConfigDict, UrlConstraints


class SongBase(BaseModel):
    title: Annotated[str, constr(max_length=100)]
    description: Annotated[str, constr(max_length=25)]
    model_config = ConfigDict(extra='allow', from_attributes=True)


class CreateSong(SongBase):
    file_url: UrlConstraints
