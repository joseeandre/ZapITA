from sqlalchemy.orm import Session
from typing import List
from models.user import User
from models.message import Message
import abc


class ABCDatawarehouseDal():

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
    def create_user(self, user: User) -> User:
        """creates user"""

    @abc.abstractmethod
    def delete_user(self, user: User):
        """creates user"""

    @abc.abstractmethod
    def get_messages(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """gets items"""

    @abc.abstractmethod
    def create_message(self, message: Message) -> Message:
        """creates item for user"""

    @abc.abstractmethod
    def update_status(self, user: User) -> User:
        """gets user by name"""


class DatawarehouseDal(ABCDatawarehouseDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_name(self, name: str) -> User:
        return self.db.query(User).filter(User.name == name).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).filter().offset(skip).limit(limit).all()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def get_messages(self, skip: int = 0, limit: int = 30) -> List[User]:
        return self.db.query(Message).filter().offset(skip).limit(limit).all()

    def create_message(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def update_status(self, user=User) -> User:
        self.db.merge(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
    #     return self.db.query(Item).offset(skip).limit(limit).all()

    # def create_user_item(self, item: Item) -> Item:
    #     self.db.add(item)
    #     self.db.commit()
    #     self.db.refresh(item)
    #     return item