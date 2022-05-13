from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.tests.utils import datawarehouse_db_path
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = f"sqlite:///{datawarehouse_db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_mock_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
