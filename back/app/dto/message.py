from typing import Optional
from venv import create
from pydantic import BaseModel, ValidationError, validator
from dto.user import User


class MessageBase(BaseModel):
    to_name: Optional[str] = None
    text: str
    model: str

    @validator('model')
    def model_private_public(cls, v):
        if v not in ['private', 'public']:
            raise ValueError('Model must be private or public')
        return v
        


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    sender_name: str

    class Config:
        orm_mode = True
