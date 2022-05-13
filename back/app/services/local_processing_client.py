import awswrangler as wr
import pandas as pd
from app.utils.settings import Settings
import abc
from typing import List


class ABCLocalProcessingClient():

    @abc.abstractmethod
    def create_catalog_db_if_not_exists(self) -> bool:
        """Creates a db in the catalog if it does not exists"""

    @abc.abstractmethod
    def get_df_from_dl_json(self, path: str) -> pd.DataFrame:
        """Get dataframe from raw json files in datalake"""

    @abc.abstractmethod
    def save_partitioned_df_to_catalog_parquet(
        self, dataframe: pd.DataFrame, path: str,
        table: str, partitions: List[str]
    ) -> bool:
        """Saves the dataframe to partioned parquet table in the catalog"""


class LocalProcessingClient(ABCLocalProcessingClient):

    def __init__(self, app_conf: Settings):
        self.config: Settings = app_conf

    def create_catalog_db_if_not_exists(self) -> bool:
        databases: pd.DataFrame = wr.catalog.databases()
        if self.config.datalake_db not in databases.values:
            wr.catalog.create_database(self.config.datalake_db)
            return True
        return False

    def get_df_from_dl_json(self, path: str) -> pd.DataFrame:
        return wr.s3.read_json(
            f"s3://{self.config.bucket}/{self.config.prefix}/" +
            "data/process-example/*.json"  # no need for *.json, just testing
        )

    def save_partitioned_df_to_catalog_parquet(
        self, dataframe: pd.DataFrame, path: str,
        table: str, partitions: List[str]
    ) -> bool:
        wr.s3.to_parquet(
            df=dataframe,
            path=path,
            dataset=True,
            database=self.config.datalake_db,
            table=table,
            mode="overwrite_partitions",
            partition_cols=partitions
        )
        return True
