from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    last_status: datetime

    class Config:
        orm_mode = True
