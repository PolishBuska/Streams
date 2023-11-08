from typing import Annotated

from pydantic import (BaseModel,
                      constr,
                      ConfigDict,
                      EmailStr,
                      Field)

from enum import Enum


class Roles(Enum):
    Listener: 1
    Publisher: 2


class UserBase(BaseModel):
    id: int
    username: Annotated[str, constr(max_length=25)]
    email: EmailStr
    password: Annotated[str, constr(max_length=50)]
    role_id: Roles
    model_config = ConfigDict(extra='allow', from_attributes=True)


class CreateUser(UserBase):
    id: int = Field(exclude=True)


class ReturnUser(UserBase):
    password: str = Field(exclude=True)

