from pydantic import (BaseModel,
                      ConfigDict,
                      FilePath)


class FileBase(BaseModel):

    filename: str
    url: FilePath
    model_config = ConfigDict(extra='allow', from_attributes=True)

