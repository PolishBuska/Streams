from typing import Annotated
from pydantic import (BaseModel,
                      constr,
                      ConfigDict)

from app.schemas.file import FileBase


class SongBase(BaseModel):
    id: int
    title: Annotated[str, constr(max_length=100)]
    description: Annotated[str, constr(max_length=25)]
    file: FileBase
    model_config = ConfigDict(extra='allow', from_attributes=True)


