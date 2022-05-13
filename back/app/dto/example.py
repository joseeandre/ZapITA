from pydantic import BaseModel
import datetime


class Example(BaseModel):
    code: str
    date: datetime.date
    px_last: float
