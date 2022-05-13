from dto.user import User, UserCreate
from models.user import User as UserModel
from dto.message import Message, MessageCreate
from models.message import Message as MessageModel
from dal.chatuol import ABCDatawarehouseDal
from fastapi import HTTPException
from typing import List
from pydantic import parse_obj_as
import abc
import time, threading
from datetime import datetime
import json

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

class ABCChatUolService():

    @abc.abstractmethod
    def get_user(self, user_id: int) -> User:
        """gets user by id"""

    @abc.abstractmethod
    def get_user_by_name(self, name: str) -> User:
        """gets user by name"""

    @abc.abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """gets online users"""

    @abc.abstractmethod
    def create_user(self, user: UserCreate) -> User:
        """creates user"""

    @abc.abstractmethod
    def get_messages(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """gets items"""

    @abc.abstractmethod
    def create_message(self, message: MessageCreate, sender: str) -> Message:
        """creates item for user"""

    @abc.abstractmethod
    def update_status(self, user: UserCreate) -> User:
        """gets user by name"""


class DatawarehouseService(ABCChatUolService):

    def __init__(self, dw_dal: ABCDatawarehouseDal):
        self.dal: ABCDatawarehouseDal = dw_dal

    def get_user(self, user_id: int) -> User:
        user = self.dal.get_user(user_id)
        return User.from_orm(user) if user is not None else None

    def get_user_by_name(self, name: str) -> User:
        user = self.dal.get_user_by_name(name)
        return User.from_orm(user) if user is not None else None

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return parse_obj_as(List[User], self.dal.get_users(skip, limit))

    def create_user(self, user: UserCreate) -> User:
        current_user = self.dal.get_user_by_name(user.name)
        if current_user:
            raise HTTPException(
                status_code=400, detail="Name already in use"
            )
        db_user = UserModel(name=user.name)
        return User.from_orm(self.dal.create_user(user=db_user))

    def get_messages(self, skip: int = 0, limit: int = 100) -> List[Message]:
        return parse_obj_as(List[Message], self.dal.get_messages(skip, limit))

    def create_message(self, message: MessageCreate, sender: str) -> Message:
        db_message = MessageModel(**message.dict(), sender_name=sender)
        return Message.from_orm(self.dal.create_message(message=db_message))

    def update_status(self, user: UserCreate) -> User:
        db_user = self.dal.get_user_by_name(user.name)
        if db_user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        db_user.last_status = datetime.now()
        return User.from_orm(self.dal.update_status(user=db_user))

