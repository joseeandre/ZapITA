from factories.config import get_settings
from utils.settings import Settings
from fastapi import APIRouter
from typing import List
from fastapi import Depends, HTTPException
from services.chatuol import ABCChatUolService
from dto.user import User, UserCreate
from dto.message import Message, MessageCreate
from factories.chatuol import get_datawarehouse_service


router = APIRouter()


@router.post("/users", response_model=User)
async def create_user(
    user: UserCreate,
    service: ABCChatUolService = Depends(get_datawarehouse_service)
):
    return service.create_user(user=user)


@router.get("/users", response_model=List[User])
async def read_users(
    skip: int = 0, limit: int = 100,
    service: ABCChatUolService = Depends(get_datawarehouse_service)
):
    return service.get_users(skip=skip, limit=limit)

@router.post("/messages", response_model=Message)
async def creat_message(
    message: MessageCreate,
    service: ABCChatUolService = Depends(get_datawarehouse_service)
):
    return service.create_message(message=message, sender="jose")

@router.get("/messages", response_model=List[Message])
async def read_messagess(
    skip: int = 0, limit: int = 100,
    service: ABCChatUolService = Depends(get_datawarehouse_service)
):
    return service.get_messages(skip=skip, limit=limit)

# @router.put("/messages/{message_id}", response_model=Message)
# async def edit_message(
#     user: UserCreate,
#     service: ABCChatUolService = Depends(get_datawarehouse_service)
# ):
#     return service.create_user(user=user)

# @router.delete("/messages/{message_id}")
# async def delete_message(
#     skip: int = 0, limit: int = 100,
#     service: ABCChatUolService = Depends(get_datawarehouse_service)
# ):
#     return service.get_users(skip=skip, limit=limit)

@router.post("/status", response_model=User)
async def update_status(
    user: UserCreate,
    service: ABCChatUolService = Depends(get_datawarehouse_service)
):
    return service.update_status(user=user)


# @router.get("/users/{user_id}", response_model=User)
# async def read_user(
#     user_id: int,
#     service: ABCChatUolService = Depends(get_datawarehouse_service)
# ):
#     user = service.get_user(user_id=user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @router.post("/users/{user_id}/items", response_model=Item)
# async def create_item_for_user(
#     user_id: int, item: ItemCreate,
#     service: ABCChatUolService = Depends(get_datawarehouse_service)
# ):
#     return service.create_user_item(item=item, user_id=user_id)


# @router.get("/user-items", response_model=List[Item])
# async def read_items(
#     skip: int = 0, limit: int = 100,
#     service: ABCChatUolService = Depends(get_datawarehouse_service)
# ):
#     return service.get_items(skip=skip, limit=limit)


@router.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
    }
