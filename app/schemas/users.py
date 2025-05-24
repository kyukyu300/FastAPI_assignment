from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'


class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum

class UserUpdateRequest(BaseModel):
    username: str | None = None
    age: int | None = None


class UserSearchParams(BaseModel):
    class Config:
        extra = "forbid"

    username: Optional[str] = None
    age: Optional[conint(gt=0)] = None
    gender: Optional[GenderEnum] = None