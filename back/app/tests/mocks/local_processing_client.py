from app.services.local_processing_client import ABCLocalProcessingClient
import pandas as pd
from typing import List


class MLocalProcessingClient(ABCLocalProcessingClient):

    def create_catalog_db_if_not_exists(self) -> bool:
        return True

    def get_df_from_dl_json(self, path: str) -> pd.DataFrame:
        return pd.read_json("app/tests/resources/mock_data.json")

    def save_partitioned_df_to_catalog_parquet(
        self, dataframe: pd.DataFrame, path: str,
        table: str, partitions: List[str]
    ) -> bool:
        return True


def get_mock_local_processing_client():
    client = MLocalProcessingClient()
    try:
        yield client
    finally:
        pass
