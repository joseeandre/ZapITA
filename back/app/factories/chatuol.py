from dal.chatuol import DatawarehouseDal, ABCDatawarehouseDal
from fastapi import Depends
from factories.db_session import get_db
from sqlalchemy.orm import Session
from services.chatuol import DatawarehouseService
from services.chatuol import ABCChatUolService


def get_datawarehouse_dal(
    db: Session = Depends(get_db)
) -> ABCDatawarehouseDal:
    dal = DatawarehouseDal(db)
    try:
        yield dal
    finally:
        pass


def get_datawarehouse_service(
    dal: ABCDatawarehouseDal = Depends(get_datawarehouse_dal)
) -> ABCChatUolService:
    service = DatawarehouseService(dal)
    try:
        yield service
    finally:
        pass
