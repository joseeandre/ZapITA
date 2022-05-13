from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from dal.dw_database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    last_status = Column(DateTime, default=datetime.now())
