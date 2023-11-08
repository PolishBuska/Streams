from typing import Annotated

from pydantic import BaseModel, constr, ConfigDict

from app.schemas.song import SongBase


class SongFileSchema(BaseModel):
    file_name: Annotated[str, constr(max_length=100)]
    link: Annotated[str, constr(max_length=25)]
    model_config = ConfigDict(extra='ignore', from_attributes=True)


class FullDataFileSong(SongBase):
    pass
