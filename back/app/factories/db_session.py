from dal.dw_database import SessionLocal
from sqlalchemy.orm import Session


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
