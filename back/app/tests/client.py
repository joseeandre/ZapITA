from app.main import app
from fastapi.testclient import TestClient
from app.factories.cloud_clients import get_storage_client
from app.tests.mocks.storage_client import get_mock_storage_client
from app.factories.datalake import get_datalake_query_client
from app.tests.mocks.datalake_query_client \
    import get_mock_datalake_query_client
from yoyo import get_backend
from yoyo import read_migrations
from app.tests.utils import datalake_db_path, datawarehouse_db_path
import os
from app.factories.db_session import get_db
from app.factories.datalake import get_local_processing_client
from app.tests.mocks.db_session import get_mock_db, engine
from app.tests.mocks.local_processing_client \
    import get_mock_local_processing_client
from app.dal.dw_database import Base


class APITestClient():

    def _apply_migration(self, db_path: str, migration_path: str):
        backend = get_backend(f"sqlite:///{db_path}")
        migrations = read_migrations(migration_path)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def __init__(self):
        self.client = TestClient(app)
        app.dependency_overrides[get_storage_client] = get_mock_storage_client
        app.dependency_overrides[get_datalake_query_client] = \
            get_mock_datalake_query_client
        app.dependency_overrides[get_db] = get_mock_db
        app.dependency_overrides[get_local_processing_client] = \
            get_mock_local_processing_client

        Base.metadata.create_all(bind=engine)

        self._apply_migration(
            datalake_db_path, "app/tests/migrations/datalake")
        self._apply_migration(
            datawarehouse_db_path, "app/tests/migrations/datawarehouse")

    def __del__(self):
        os.remove(datalake_db_path)
        os.remove(datawarehouse_db_path)
