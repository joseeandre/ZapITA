from app.dal.datalake_query_client import ABCDatalakeQueryClient
import sqlite3
import pandas as pd
from app.tests.utils import datalake_db_path


class MDatalakeQueryClient(ABCDatalakeQueryClient):

    def __init__(self):
        self.conn = sqlite3.connect(datalake_db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def run_query(self, query: str) -> pd.DataFrame:
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.description]
        rows = self.cursor.fetchall()
        data = [
            {
                k: v for k, v in dict(zip(columns, row)).items()
                if v is not None
            } for row in rows
        ]
        return pd.DataFrame(data)


def get_mock_datalake_query_client():
    client = MDatalakeQueryClient()
    try:
        yield client
    finally:
        client.conn.close()
