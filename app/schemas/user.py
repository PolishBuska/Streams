from enum import Enum
from typing import Annotated

from pydantic import (BaseModel,
                      EmailStr,
                      ConfigDict)
from pydantic.types import constr


class Roles(int, Enum):
    Listener = 1
    Publisher = 2


class UserBase(BaseModel):
    nickname: Annotated[str, constr(max_length=25)]
    email: EmailStr
    role_id: Roles
    model_config = ConfigDict(extra='ignore', from_attributes=True)


class CreateUser(UserBase):
    password: Annotated[str, constr(max_length=50)]


class ReturnUser(UserBase):
    id: int

