from app.tests.client import APITestClient
from typing import List
from pydantic import parse_obj_as
from app.dto.example import Example


class Test_DatalakeControllerSpec():

    @classmethod
    def setup_class(cls):
        cls.test_client: APITestClient = APITestClient()

    @classmethod
    def teardown_class(cls):
        cls.test_client.__del__()

    def test_add_cvm_funds_positions_to_datalake(self):
        response = self.test_client.client \
            .post("/data-lake/storage/cvm-funds-positions")
        assert response.status_code == 200
        assert response.json()

    def test_get_example(self):
        response = self.test_client.client \
            .get("/data-lake/example")
        assert response.status_code == 200

        example_data = parse_obj_as(List[Example], response.json())
        assert len(example_data) == 10

    def test_process_example_parquet(self):
        response = self.test_client.client \
            .post("/data-lake/processing/example")
        assert response.status_code == 200
        assert response.json()
