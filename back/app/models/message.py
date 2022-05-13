from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from dal.dw_database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    model = Column(String, index=True)
    to_name = Column(String, ForeignKey("users.name"))
    sender_name = Column(String, ForeignKey("users.name"))
